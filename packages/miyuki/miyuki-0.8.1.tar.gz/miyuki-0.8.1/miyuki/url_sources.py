# --- START OF FILE miyuki/url_sources.py ---

from abc import ABC, abstractmethod
import re
from typing import Optional
# from miyuki.http_client import HttpClient # No longer needed
from miyuki.config import HREF_REGEX_PUBLIC_PLAYLIST, HREF_REGEX_NEXT_PAGE, MATCH_UUID_PATTERN
from miyuki.logger import logger
from miyuki.utils import ThreadSafeCounter
from enum import Enum
import cloudscraper # Use cloudscraper
from urllib.parse import urljoin # Needed for SearchSource

class UrlType(Enum):
    SINGLE = 1
    PLAYLIST = 2

class UrlSource(ABC):
    @abstractmethod
    def get_urls(self) -> list[str]:
        pass

    @staticmethod
    def movie_count_log(movie_counter: ThreadSafeCounter, movie_url: str):
        count = movie_counter.increment_and_get() # Get count first
        logger.info(f"Identified Movie URL #{count}: {movie_url}") # Log count and URL

    @staticmethod
    def get_urls_from_list(movie_counter: ThreadSafeCounter, play_list_url: str, limit: Optional[int], scraper: cloudscraper.CloudScraper, cookie=None) -> list[str]: # Accept scraper
        movie_url_list = []
        url = play_list_url
        base_url = "/".join(play_list_url.split("/")[:3]) # Extract base URL like https://missav.ai
        logger.info(f"[get_urls_from_list] Starting playlist processing for URL: {url}, Limit: {limit}, Base: {base_url}")
        page_count = 0
        # Make sure limit comparison works (limit is int | None)
        while url and (limit is None or movie_counter.get() < limit):
            page_count += 1
            current_page_url = url # Store the URL for this iteration
            logger.info(f"[get_urls_from_list] Fetching page {page_count} URL: {current_page_url}")

            try:
                 response = scraper.get(current_page_url, cookies=cookie, timeout=20) # Use scraper
                 response.raise_for_status() # Check for HTTP errors (4xx, 5xx)
                 html_source = response.text # Use .text for decoded string
                 logger.debug(f"[get_urls_from_list] Successfully fetched HTML for: {current_page_url}")
                 # Save the HTML for debugging playlist issues if needed
                 # with open(f"debug_playlist_page_{page_count}.html", "w", encoding="utf-8") as pf: pf.write(html_source)
            except cloudscraper.exceptions.CloudflareException as e:
                 logger.error(f"[get_urls_from_list] Cloudflare challenge failed for {current_page_url}: {e}")
                 break # Stop processing this playlist if blocked
            except Exception as e:
                 logger.error(f"[get_urls_from_list] Failed to fetch HTML for page URL {current_page_url}: {e}")
                 break # Stop processing this playlist on other errors

            # --- Find Movie Links ---
            # Check if HREF_REGEX_PUBLIC_PLAYLIST is still valid for the site structure
            # Example: '<a href="([^"]+)" alt="[^"]*">' might be too specific if 'alt' is missing
            # A potentially more robust pattern might just look for links within specific list items:
            # Example: '<div class="card-body">\s*<a href="([^"]+)"' (NEEDS INSPECTION of playlist HTML)
            movie_url_matches = re.findall(HREF_REGEX_PUBLIC_PLAYLIST, html_source)
            logger.info(f"[get_urls_from_list] Found {len(movie_url_matches)} potential movie links using pattern '{HREF_REGEX_PUBLIC_PLAYLIST}' on page {page_count}.")
            logger.debug(f"[get_urls_from_list] Links found: {movie_url_matches}")

            temp_url_list = list(set(movie_url_matches)) # Get unique URLs from this page
            logger.info(f"[get_urls_from_list] Found {len(temp_url_list)} unique potential movie links on page {page_count}.")

            added_count_this_page = 0
            for movie_url_relative in temp_url_list:
                # Check limit before adding and logging
                if limit is not None and movie_counter.get() >= limit:
                     logger.info(f"[get_urls_from_list] Limit ({limit}) reached. Stopping collection.")
                     return movie_url_list # Return immediately

                # Make URL absolute using the base URL
                absolute_movie_url = urljoin(base_url, movie_url_relative.strip())

                movie_url_list.append(absolute_movie_url)
                UrlSource.movie_count_log(movie_counter, absolute_movie_url) # Log happens here with increment
                added_count_this_page += 1

            logger.info(f"[get_urls_from_list] Added {added_count_this_page} new URLs from page {page_count}. Total collected so far: {len(movie_url_list)}")

            # Check limit again after processing the page, before finding next page
            if limit is not None and movie_counter.get() >= limit:
                 logger.info(f"[get_urls_from_list] Limit ({limit}) reached after processing page. Stopping collection.")
                 return movie_url_list # Return immediately

            # --- Find Next Page Link ---
            # Check if HREF_REGEX_NEXT_PAGE is still valid
            next_page_matches = re.findall(HREF_REGEX_NEXT_PAGE, html_source)
            if next_page_matches:
                next_page_relative_url = next_page_matches[0].replace('&', '&')
                # Make the next page URL absolute relative to the *current page's* full URL
                # OR assume it's relative to the base_url - needs checking on the site
                # Let's assume relative to base_url for now
                url = urljoin(base_url, next_page_relative_url)
                logger.info(f"[get_urls_from_list] Found next page link: {url}")
            else:
                logger.info(f"[get_urls_from_list] No next page link found on page {page_count}. End of playlist.")
                url = None # Stop the loop
        logger.info(f"[get_urls_from_list] Finished playlist processing for {play_list_url}. Total URLs collected: {len(movie_url_list)}")
        return movie_url_list

class SingleUrlSource(UrlSource):
    # No changes needed here, doesn't make HTTP requests directly
    def __init__(self, movie_counter: ThreadSafeCounter, url: str, limit: Optional[int]):
        self.movie_counter = movie_counter
        self.url = url
        self.limit = limit
        logger.info(f"[SingleUrlSource.__init__] Initialized for URL: {self.url}, Limit: {self.limit}")

    def get_urls(self) -> list[str]:
        logger.info(f"[SingleUrlSource.get_urls] Checking URL: {self.url}")
        if self.limit is not None and self.movie_counter.get() >= self.limit: # Check limit before adding
            logger.info(f"[SingleUrlSource.get_urls] Limit ({self.limit}) reached. Skipping URL: {self.url}")
            return []
        else:
            UrlSource.movie_count_log(self.movie_counter, self.url)
            logger.info(f"[SingleUrlSource.get_urls] Returning URL: {self.url}")
            return [self.url]

class PlaylistSource(UrlSource):
    # Accept scraper in __init__
    def __init__(self, movie_counter: ThreadSafeCounter, playlist_url: str, limit: Optional[int], scraper: cloudscraper.CloudScraper):
        self.movie_counter = movie_counter
        self.playlist_url = playlist_url
        self.limit = limit
        self.scraper = scraper # Store the passed scraper
        logger.info(f"[PlaylistSource.__init__] Initialized for Playlist URL: {self.playlist_url}, Limit: {self.limit}")

    def get_urls(self) -> list[str]:
        logger.info(f"[PlaylistSource.get_urls] Starting processing for playlist: {self.playlist_url}")
        # Pass the stored scraper
        result_urls = UrlSource.get_urls_from_list(movie_counter=self.movie_counter, play_list_url=self.playlist_url, limit=self.limit, scraper=self.scraper, cookie=None)
        logger.info(f"[PlaylistSource.get_urls] Finished processing for {self.playlist_url}. Found {len(result_urls)} URLs.")
        return result_urls

class AutoUrlSource(UrlSource):
     # Accept scraper in __init__
    def __init__(self, movie_counter: ThreadSafeCounter, auto_urls: list[str], limit: Optional[str], scraper: cloudscraper.CloudScraper):
        self.movie_counter = movie_counter
        self.auto_urls = auto_urls
        # Convert limit to int here, handling None
        self.limit = int(limit) if limit else None
        self.scraper = scraper # Store the passed scraper
        logger.info(f"[AutoUrlSource.__init__] Initialized with URLs: {self.auto_urls}, Limit: {self.limit}")

    def get_urls(self) -> list[str]:
        movie_url_list = []
        logger.info(f"[AutoUrlSource.get_urls] Starting processing for {len(self.auto_urls)} provided URLs.")

        for url in self.auto_urls:
            logger.info(f"[AutoUrlSource.get_urls] Processing input URL: {url}")

            # Check limit before even determining type
            if self.limit is not None and self.movie_counter.get() >= self.limit:
                logger.info(f"[AutoUrlSource.get_urls] Limit ({self.limit}) reached. Skipping further URL processing.")
                break # Stop processing more URLs from the input list

            # Pass scraper when determining type
            url_type : Optional[UrlType] = self._determine_url_type(url, self.scraper)
            logger.info(f"[AutoUrlSource.get_urls] Determined URL type for {url}: {url_type}")

            sub_source_urls = []
            if url_type == UrlType.SINGLE:
                logger.info(f"[AutoUrlSource.get_urls] Treating {url} as SINGLE. Creating SingleUrlSource.")
                # SingleUrlSource doesn't need scraper passed to it
                single_url_source = SingleUrlSource(movie_counter=self.movie_counter, url=url, limit=self.limit)
                sub_source_urls = single_url_source.get_urls()
                logger.info(f"[AutoUrlSource.get_urls] SingleUrlSource for {url} returned {len(sub_source_urls)} URL(s).")
            elif url_type == UrlType.PLAYLIST:
                logger.info(f"[AutoUrlSource.get_urls] Treating {url} as PLAYLIST. Creating PlaylistSource.")
                # Pass the scraper to PlaylistSource
                playlist_source = PlaylistSource(movie_counter=self.movie_counter, playlist_url=url, limit=self.limit, scraper=self.scraper)
                sub_source_urls = playlist_source.get_urls()
                logger.info(f"[AutoUrlSource.get_urls] PlaylistSource for {url} returned {len(sub_source_urls)} URL(s).")
            else:
                logger.warning(f"[AutoUrlSource.get_urls] Could not determine type for URL: {url}. Skipping.")

            if sub_source_urls:
                 # Ensure URLs are unique if accumulating from multiple sources
                 # Although PlaylistSource already handles uniqueness per page
                 movie_url_list.extend(u for u in sub_source_urls if u not in movie_url_list)
                 logger.info(f"[AutoUrlSource.get_urls] Added {len(sub_source_urls)} unique URL(s) to main list. Total now: {len(movie_url_list)}")

        logger.info(f"[AutoUrlSource.get_urls] Finished processing all input URLs. Final list size: {len(movie_url_list)}")
        return movie_url_list

    # Modify _determine_url_type to accept scraper
    def _determine_url_type(self, url: str, scraper: cloudscraper.CloudScraper) -> Optional[UrlType]:
        logger.info(f"[AutoUrlSource._determine_url_type] Checking URL: {url}")
        try:
            # Pass scraper to _is_movie_url
            is_movie = self._is_movie_url(url, scraper)
            logger.info(f"[AutoUrlSource._determine_url_type] Result of _is_movie_url for {url}: {is_movie}")
            if is_movie:
                logger.info(f"[AutoUrlSource._determine_url_type] Determined type: SINGLE for {url}")
                return UrlType.SINGLE
            else:
                # Add a check here? Could try fetching as playlist and see if it finds links?
                # For now, stick to the original logic: if not movie -> playlist
                logger.info(f"[AutoUrlSource._determine_url_type] Determined type: PLAYLIST for {url}")
                return UrlType.PLAYLIST
        except Exception as e:
             logger.error(f"[AutoUrlSource._determine_url_type] Error determining type for {url}: {e}", exc_info=True)
             return None # Indicate failure

    # Modify _is_movie_url to accept scraper
    def _is_movie_url(self, url: str, scraper: cloudscraper.CloudScraper) -> bool:
        logger.info(f"[AutoUrlSource._is_movie_url] Attempting to fetch HTML for URL type check: {url}")
        try:
             response = scraper.get(url, timeout=20)
             response.raise_for_status()
             html_str = response.text # Use text
             logger.info(f"[AutoUrlSource._is_movie_url] Successfully fetched and decoded HTML for {url}.")
             # Save the HTML we actually get AFTER Cloudflare attempt
        except cloudscraper.exceptions.CloudflareException as e:
             logger.error(f"[AutoUrlSource._is_movie_url] Cloudflare challenge failed for {url}: {e}")
             # Save the challenge page content if possible
             try:
                  with open("debug_cloudflare_challenge.html", "w", encoding="utf-8") as cf_file:
                       cf_file.write(e.response.text)
                  logger.info("Saved Cloudflare challenge page to 'debug_cloudflare_challenge.html'")
             except Exception as save_e:
                  logger.error(f"Could not save Cloudflare challenge page: {save_e}")
             return False # Treat as non-movie if challenge fails
        except Exception as e:
             logger.warning(f"[AutoUrlSource._is_movie_url] Failed to fetch HTML for {url}: {e}. Cannot determine if it's a movie URL.")
             return False

        # Now try the regex on html_str
        match = re.search(MATCH_UUID_PATTERN, html_str, re.DOTALL) # Use the pattern from config

        if not match:
             logger.info(f"[AutoUrlSource._is_movie_url] Regex pattern to find eval block did NOT match for {url}. Assuming not a movie URL.")
             return False
        else:
             # We don't need the group here, just that it matched.
             logger.info(f"[AutoUrlSource._is_movie_url] Regex pattern to find eval block matched for {url}. Assuming it IS a movie URL.")
             return True

# --- Modify AuthSource ---
class AuthSource(UrlSource):
     # Accept scraper in __init__
    def __init__(self, movie_counter: ThreadSafeCounter, username: str, password: str, limit: Optional[str], scraper: cloudscraper.CloudScraper):
        self.movie_counter = movie_counter
        self.scraper = scraper # Store scraper
        self.limit = int(limit) if limit else None
        # Login needs to use the scraper now
        self.cookie = self._login(username, password) # Store cookies returned by login if needed

    def _login(self, username: str, password: str) -> Optional[dict]: # Return Optional dict
        logger.info(f"Attempting login for user: {username}")
        try:
            # Use scraper.post
            response = self.scraper.post('https://missav.ai/api/login', data={'email': username, 'password': password}, timeout=20)
            logger.debug(f"Login response status: {response.status_code}")
            logger.debug(f"Login response headers: {response.headers}")
            logger.debug(f"Login response content snippet: {response.text[:200]}") # Log snippet
            response.raise_for_status() # Check for HTTP errors

            if response.status_code == 200:
                # Check if login was actually successful based on response content or cookies set
                # This part is tricky without knowing the exact API response for success/fail
                # Let's assume for now it worked and cloudscraper handles session cookies
                logger.info(f"Login request seems successful (Status 200). Relying on cloudscraper session cookies.")
                return self.scraper.cookies.get_dict() # Return current session cookies
            else:
                # This part might not be reached if raise_for_status catches the error
                logger.error(f"Login request failed with status: {response.status_code}")
                exit(MAGIC_NUMBER)
        except cloudscraper.exceptions.CloudflareException as e:
             logger.error(f"Cloudflare challenge failed during login: {e}")
             exit(MAGIC_NUMBER)
        except Exception as e:
             logger.error(f"Login failed: Check network or account info. Error: {e}")
             exit(MAGIC_NUMBER)
        # Added return None for clarity if exit doesn't happen
        return None

    def get_urls(self) -> list[str]:
        url = 'https://missav.ai/saved'
        logger.info(f"Fetching saved URLs from: {url}")
        if self.cookie is None:
             logger.error("Login failed previously, cannot fetch saved URLs.")
             return []
        # Pass the scraper to get_urls_from_list.
        # Cookies are managed by the scraper's session after successful login.
        return UrlSource.get_urls_from_list(movie_counter=self.movie_counter, play_list_url=url, limit=self.limit, scraper=self.scraper, cookie=None)

# --- Modify SearchSource ---
class SearchSource(UrlSource):
     # Accept scraper in __init__
    def __init__(self, movie_counter: ThreadSafeCounter, key: str, scraper: cloudscraper.CloudScraper, cookies: Optional[dict] = None): # Added scraper
        self.movie_counter = movie_counter
        self.key = key
        self.scraper = scraper # Store scraper
        self.cookies = cookies # Keep cookies if needed

    def get_urls(self) -> list[str]:
        search_url = f"https://missav.ai/search/{self.key}"
        # Define base URL for resolving relative links found
        base_url = "https://missav.ai"
        # Escape key for safety in regex and use the public playlist regex
        search_regex = HREF_REGEX_PUBLIC_PLAYLIST # Use the same regex as playlists
        logger.info(f"Searching for key '{self.key}' at URL: {search_url}")

        try:
            # Use scraper.get
            response = self.scraper.get(search_url, cookies=self.cookies, timeout=20)
            response.raise_for_status()
            html_source = response.text # Use .text
            logger.debug(f"Successfully fetched search results page for key '{self.key}'")
            # Save for debugging if needed
            # with open(f"debug_search_{self.key}.html", "w", encoding="utf-8") as sf: sf.write(html_source)
        except cloudscraper.exceptions.CloudflareException as e:
             logger.error(f"Cloudflare challenge failed during search for key '{self.key}': {e}")
             return []
        except Exception as e:
             logger.error(f"Search failed for key '{self.key}': {e}")
             return []

        # Find all links matching the playlist pattern
        movie_url_matches = re.findall(search_regex, html_source)
        logger.info(f"Found {len(movie_url_matches)} potential matches on search results page.")

        # Filter results to find the specific key if needed, or just take the first one
        # The original regex r'<a href="([^"]+)" alt="' + self.key + '" >' tried to match the alt tag.
        # If HREF_REGEX_PUBLIC_PLAYLIST doesn't include alt, we might need a different approach
        # or iterate through matches and check their text/alt tags if necessary.
        # For now, let's assume the first match is the desired one if any are found.

        if movie_url_matches:
             # Take the first unique relative URL found
             first_relative_url = list(set(movie_url_matches))[0]
             # Make it absolute
             absolute_url = urljoin(base_url, first_relative_url.strip())

             logger.info(f"Search for '{self.key}' successful. Using first found URL: {absolute_url}")
             UrlSource.movie_count_log(self.movie_counter, absolute_url)
             return [absolute_url] # Return list with one URL
        else:
             logger.error(f"Search key '{self.key}' did not yield any matching links on the results page using pattern '{search_regex}'.")
             return []

# --- Modify FileSource ---
class FileSource(UrlSource):
     # Accept scraper in __init__
    def __init__(self, movie_counter: ThreadSafeCounter, file_path: str, limit: Optional[str], scraper: cloudscraper.CloudScraper): # Added scraper
        self.movie_counter = movie_counter
        self.file_path = file_path
        self.limit = int(limit) if limit else None
        self.scraper = scraper # Store scraper
        logger.info(f"Initializing FileSource with path: {self.file_path}")

    def get_urls(self) -> list[str]:
        logger.info(f"Reading URLs from file: {self.file_path}")
        try:
             with open(self.file_path, 'r', encoding='utf-8') as f:
                # Read lines, strip whitespace, filter out empty lines
                urls = [line.strip() for line in f if line.strip()]
             logger.info(f"Read {len(urls)} URLs from file.")
        except FileNotFoundError:
             logger.error(f"File not found: {self.file_path}")
             return []
        except Exception as e:
             logger.error(f"Error reading file {self.file_path}: {e}")
             return []

        if not urls:
             logger.warning(f"No valid URLs found in file: {self.file_path}")
             return []

        # Pass the scraper to AutoUrlSource instance created here
        # Ensure limit is passed correctly (as string or None)
        limit_str = str(self.limit) if self.limit is not None else None
        logger.info(f"Creating AutoUrlSource for file content with limit: {limit_str}")
        auto_url_source = AutoUrlSource(movie_counter=self.movie_counter, auto_urls=urls, limit=limit_str, scraper=self.scraper)
        return auto_url_source.get_urls()

# --- END OF FILE miyuki/url_sources.py ---