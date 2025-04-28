import os
import re
from typing import Optional, Tuple
import threading
from miyuki.config import ( # Make sure to import all needed config vars
    MOVIE_SAVE_PATH_ROOT, MATCH_UUID_PATTERN, MATCH_TITLE_PATTERN, COVER_URL_PREFIX,
    TMP_HTML_FILE, RESOLUTION_PATTERN, VIDEO_M3U8_PREFIX, VIDEO_PLAYLIST_SUFFIX
)
from miyuki.logger import logger
from miyuki.utils import ThreadSafeCounter, display_progress_bar, split_integer_into_intervals, find_last_non_empty_line, find_closest
from miyuki.ffmpeg_processor import FFmpegProcessor
import cloudscraper


class VideoDownloader:
    def __init__(self, url: str, scraper: cloudscraper.CloudScraper, options: dict):
        self.url = url
        self.scraper = scraper # Store scraper instance
        self.movie_name = url.split('/')[-1]
        self.movie_folder = os.path.join(MOVIE_SAVE_PATH_ROOT, self.movie_name)
        self.options = options
        self.uuid = None
        self.title = None
        self.final_file_name = None
        self.counter = ThreadSafeCounter()

    def _fetch_metadata(self) -> bool:
        try:
            # Use scraper.get().text for HTML processing
            response = self.scraper.get(self.url, timeout=20)
            response.raise_for_status()
            html = response.text # Use .text
        except cloudscraper.exceptions.CloudflareException as e:
             logger.error(f"Cloudflare challenge failed fetching metadata for {self.url}: {e}")
             return False
        except Exception as e:
             logger.error(f"Failed to fetch HTML for {self.url}: {e}")
             return False

        # No decode needed

        with open(TMP_HTML_FILE, 'w', encoding='utf-8') as file:
            file.write(html)

        # Use the NEW pattern, and add re.DOTALL in case the JS is multiline
        match = re.search(MATCH_UUID_PATTERN, html, re.DOTALL)
        if not match:
            # Add a log if the *old* pattern is found, indicating partial regression or A/B testing by the site
            old_pattern_match = re.search(r'm3u8\|([a-f0-9\|]+)\|com\|surrit\|https\|video', html)
            if old_pattern_match:
                logger.warning("Found OLD UUID pattern structure. Website might be inconsistent. Trying to parse new structure failed.")
            else:
                logger.error("Failed to match new UUID pattern structure (eval block).")
            return False

        # --- Logic to process the captured split string ---
        # *** IMPORTANT: Adjust group index based on the final regex ***
        # If using: r"eval\(function\(p,a,c,k,e,d\)\{.*?\}\((['\"])(.*?)\1\s*\.\s*split\(\s*'\|'\s*\)"
        # The content is in Group 2
        split_string_content = match.group(2) # <-- USE GROUP 2
        logger.info("Successfully matched eval split string content.")
        logger.debug(f"Split string content raw: '{split_string_content}'")

        parts = split_string_content.split('|')
        logger.debug(f"Split parts array (length {len(parts)}): {parts}")

        required_indices = [1, 2, 3, 4, 5]
        if not all(i < len(parts) for i in required_indices):
             logger.error(f"Split parts array does not contain all expected indices [1-5] for UUID. Cannot construct UUID.")
             logger.debug(f"Available parts: {parts}")
             return False

        try:
             self.uuid = f"{parts[5]}-{parts[4]}-{parts[3]}-{parts[2]}-{parts[1]}"
             logger.info(f"Constructed UUID successfully: {self.uuid}")
        except IndexError:
             logger.error(f"Error accessing expected indices [1-5] in split parts array during UUID construction.")
             logger.debug(f"Available parts: {parts}")
             return False

        # --- Title extraction remains the same ---
        title_match = re.search(MATCH_TITLE_PATTERN, html)
        if title_match:
            illegal_chars = r'[<>:"/\\|?*\s]+' # Use regex for illegal chars + whitespace
            origin_title = title_match.group(1).strip() # Added strip()
            # Replace sequences of illegal chars/spaces with a single underscore
            safe_title = re.sub(illegal_chars, '_', origin_title)
            # Remove leading/trailing underscores that might result
            safe_title = safe_title.strip('_')

            if "uncensored" in self.url.lower(): # Use lower() for case-insensitivity
                safe_title += "_uncensored"
            self.title = safe_title
            logger.info(f"Found title: '{origin_title}', Sanitized: '{self.title}'")
        else:
             logger.warning(f"Could not extract title for {self.url}")
             self.title = None # Ensure title is None if not found
        # --- End of Title extraction ---

        return True

    def _download_cover(self) -> None:
        if not self.options.get('cover_action'): return
        cover_url = f"{COVER_URL_PREFIX}{self.movie_name}/cover-n.jpg"
        try:
             # Use scraper.get().content for image bytes
             response = self.scraper.get(cover_url, timeout=15)
             response.raise_for_status()
             cover_content = response.content # Use .content
        except Exception as e:
             logger.error(f"Failed to download cover for {self.movie_name}: {e}")
             return # Don't proceed if download fails

        cover_path = os.path.join(MOVIE_SAVE_PATH_ROOT, f"{self.movie_name}-cover.jpg")
        try:
             with open(cover_path, 'wb') as f:
                  f.write(cover_content)
             logger.info(f"Cover downloaded successfully to {cover_path}")
        except IOError as e:
             logger.error(f"Failed to save cover to {cover_path}: {e}")

    def _get_final_quality_and_resolution(self, playlist: str) -> Tuple[Optional[str], Optional[str]]:
         # This function takes playlist content as string, no scraper needed here directly
        matches = re.findall(RESOLUTION_PATTERN, playlist)
        quality_map = {height: width for width, height in matches}
        quality_list = list(quality_map.keys())
        if not quality_list:
            logger.error("No resolutions found in playlist.")
            return None, None
        quality = self.options.get('quality')
        if quality is None:
            final_quality = quality_list[-1] + 'p'
            resolution_url = find_last_non_empty_line(playlist)
        else:
            target = int(quality)
            closest_height = find_closest([int(h) for h in quality_list], target)
            final_quality = str(closest_height) + 'p'
            url_type_x = f"{quality_map[str(closest_height)]}x{closest_height}/video.m3u8"
            url_type_p = f"{closest_height}p/video.m3u8"
            resolution_url = url_type_x if url_type_x in playlist else url_type_p if url_type_p in playlist else find_last_non_empty_line(playlist)
        return final_quality, resolution_url

    def _thread_task(self, start: int, end: int, uuid: str, resolution: str, video_offset_max: int) -> None:
        # Create a new scraper instance for each thread to potentially avoid session conflicts
        # Although maybe reusing the main one is ok? Let's try separate first.
        thread_scraper = cloudscraper.create_scraper(delay=5) # Create scraper for this thread
        
        for i in range(start, end):
            url = f"https://surrit.com/{uuid}/{resolution}/video{i}.jpeg"
            try:
                 # Use thread_scraper.get().content
                 retry_count = self.options.get('retry', 5)
                 delay = self.options.get('delay', 2)
                 timeout = self.options.get('timeout', 10)
                 content = None
                 for attempt in range(retry_count):
                      try:
                           response = thread_scraper.get(url, timeout=timeout)
                           response.raise_for_status()
                           content = response.content # Use .content
                           break # Success, exit retry loop
                      except Exception as thread_e:
                           logger.warning(f"Segment {i} failed (attempt {attempt + 1}/{retry_count}): {thread_e}. Retrying in {delay}s...")
                           time.sleep(delay) # Use time.sleep

                 if content:
                      file_path = os.path.join(self.movie_folder, f"video{i}.jpeg")
                      with open(file_path, 'wb') as f:
                            f.write(content)
                      display_progress_bar(video_offset_max + 1, self.counter)
                 else:
                      logger.error(f"Failed to download segment {i} for {self.movie_name} after {retry_count} retries.")

            except Exception as e: # Catch broader exceptions during segment download
                 logger.error(f"Unexpected error downloading segment {i} for {self.movie_name}: {e}")

    def _download_segments(self, uuid: str, resolution: str, video_offset_max: int) -> None:
        if not self.options.get('download_action'):
            return
        intervals = split_integer_into_intervals(video_offset_max + 1, self.options.get('num_threads', os.cpu_count()))
        self.counter.reset()
        threads = []
        for start, end in intervals:
            thread = threading.Thread(target=self._thread_task, args=(start, end, uuid, resolution, video_offset_max))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        self.counter.reset()

    def _check_integrity(self, video_offset_max: int) -> None:
        downloaded_files = len([f for f in os.listdir(self.movie_folder) if f.endswith('.jpeg')])
        total_files = video_offset_max + 1
        integrity = downloaded_files / total_files
        print()
        logger.info(f"File integrity for {self.movie_name}: {integrity:.2%} ({downloaded_files}/{total_files} files)")

    def _assemble_video(self, video_offset_max: int) -> None:
        if not self.options.get('write_action'):
            return
        self.final_file_name = f"{self.movie_name}_{self.final_quality}"
        output_file = os.path.join(MOVIE_SAVE_PATH_ROOT, f"{self.final_file_name}.mp4")
        if self.options.get('ffmpeg_action'):
            segment_files = [os.path.join(self.movie_folder, f"video{i}.jpeg") for i in range(video_offset_max + 1) if os.path.exists(os.path.join(self.movie_folder, f"video{i}.jpeg"))]
            cover_file = os.path.join(MOVIE_SAVE_PATH_ROOT, f"{self.movie_name}-cover.jpg") if self.options.get('cover_as_preview') and os.path.exists(os.path.join(MOVIE_SAVE_PATH_ROOT, f"{self.movie_name}-cover.jpg")) else None
            FFmpegProcessor.create_video_from_segments(segment_files, output_file, cover_file)
        else:
            with open(output_file, 'wb') as outfile:
                for i in range(video_offset_max + 1):
                    file_path = os.path.join(self.movie_folder, f"video{i}.jpeg")
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as infile:
                            outfile.write(infile.read())
        if self.options.get('title_action') and self.title:
            os.rename(output_file, os.path.join(MOVIE_SAVE_PATH_ROOT, f"{self.title}.mp4"))

    def download(self) -> None:
        if not self._fetch_metadata(): # Uses scraper
            return

        # --- Playlist fetching ---
        playlist_url = f"{VIDEO_M3U8_PREFIX}{self.uuid}{VIDEO_PLAYLIST_SUFFIX}"
        logger.info(f"Fetching main playlist: {playlist_url}")
        try:
             # Use scraper.get().text
             response = self.scraper.get(playlist_url, timeout=15)
             response.raise_for_status()
             playlist = response.text # Use .text
             logger.info("Successfully fetched main playlist.")
        except Exception as e:
             logger.error(f"Failed to fetch playlist {playlist_url}: {e}")
             return

        # No decode needed

        self.final_quality, resolution_url = self._get_final_quality_and_resolution(playlist) # Parses playlist string
        if not self.final_quality or not resolution_url: # Check both
             logger.error("Could not determine final quality or resolution URL.")
             return

        # --- Video m3u8 fetching ---
        video_m3u8_url = f"{VIDEO_M3U8_PREFIX}{self.uuid}/{resolution_url}"
        logger.info(f"Fetching video m3u8: {video_m3u8_url}")
        try:
             # Use scraper.get().text
             response = self.scraper.get(video_m3u8_url, timeout=15)
             response.raise_for_status()
             video_m3u8 = response.text # Use .text
             logger.info("Successfully fetched video m3u8.")
        except Exception as e:
             logger.error(f"Failed to fetch video m3u8 {video_m3u8_url}: {e}")
             return

        # No decode needed

        # --- Segment Offset Parsing ---
        try:
             # Make parsing more robust, find last line ending with .jpeg
             video_offset_max = -1
             lines = video_m3u8.strip().splitlines()
             for line in reversed(lines):
                  line = line.strip()
                  if line.endswith('.jpeg'):
                       match = re.search(r'video(\d+)\.jpeg', line)
                       if match:
                            video_offset_max = int(match.group(1))
                            logger.info(f"Determined max video segment index: {video_offset_max}")
                            break
             if video_offset_max == -1:
                  logger.error("Could not find segment index in video m3u8.")
                  return

        except (IndexError, ValueError, AttributeError) as e:
             logger.error(f"Failed to parse video segment index from m3u8: {e}")
             logger.debug(f"Video m3u8 content:\n{video_m3u8}")
             return

        if not os.path.exists(self.movie_folder):
             os.makedirs(self.movie_folder)

        self._download_cover() # Uses scraper
        self._download_segments(self.uuid, resolution_url.split('/')[0], video_offset_max) # Uses scraper via _thread_task
        self._check_integrity(video_offset_max)
        self._assemble_video(video_offset_max) # Does not use scraper

# Need to import time for sleep in _thread_task
import time
