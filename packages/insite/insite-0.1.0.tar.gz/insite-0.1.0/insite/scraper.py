import asyncio
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright
import time
import re


class InsiteScraper:
    def __init__(self, base_url, max_concurrent=5, debug=False, positive_filters=None, negative_filters=None):
        """
        Initialize the InsiteScraper with a base URL.
        
        Args:
            base_url (str): The base URL of the website to scrape.
            max_concurrent (int): Maximum number of concurrent page processing tasks
            debug (bool): Enable debug output
            positive_filters (list): List of strings or regex patterns that URLs must match to be processed
            negative_filters (list): List of strings or regex patterns that URLs must NOT match to be processed
        """
        self.base_url = base_url
        self.visited_urls = set()
        self.all_links = set()
        self.domain = urlparse(base_url).netloc
        self.max_concurrent = max_concurrent
        self.debug = debug
        self.queue = asyncio.Queue()
        
        # Store URL without fragments to avoid duplicates
        self.visited_pages = set()
        
        # Initialize filters
        self.positive_filters = [self._compile_filter(f) for f in (positive_filters or [])]
        self.negative_filters = [self._compile_filter(f) for f in (negative_filters or [])]
        
        # Track filtered URLs for reporting
        self.positive_filtered_count = 0
        self.negative_filtered_count = 0

    def _compile_filter(self, pattern):
        """
        Compile a filter pattern into a regex pattern or string.
        
        Args:
            pattern: String or regex pattern
            
        Returns:
            Compiled pattern for matching
        """
        if hasattr(pattern, 'search'):  # Already a regex pattern
            return pattern
        
        # Simple string pattern
        return pattern
    
    def _url_passes_filters(self, url):
        """
        Check if URL passes all filter criteria.
        
        Args:
            url (str): URL to check
            
        Returns:
            bool: True if URL passes filters, False otherwise
        """
        # Check positive filters - URL must match at least one if any are defined
        if self.positive_filters:
            passes_positive = False
            for pattern in self.positive_filters:
                if isinstance(pattern, str):
                    if pattern in url:
                        passes_positive = True
                        break
                else:  # Regex pattern
                    if pattern.search(url):
                        passes_positive = True
                        break
            
            if not passes_positive:
                self.positive_filtered_count += 1
                return False
        
        # Check negative filters - URL must not match any
        for pattern in self.negative_filters:
            if isinstance(pattern, str):
                if pattern in url:
                    self.negative_filtered_count += 1
                    return False
            else:  # Regex pattern
                if pattern.search(url):
                    self.negative_filtered_count += 1
                    return False
        
        return True

    async def __call__(self):
        """
        Find all links on the website starting from the base URL.
        
        Returns:
            list: All discoverable links on the website.
        """
        start_time = time.time()
        
        # Reset filter counters
        self.positive_filtered_count = 0
        self.negative_filtered_count = 0
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            # Start with the base URL
            self.queue.put_nowait(self.base_url)
            
            # Create workers
            workers = []
            for i in range(self.max_concurrent):
                context = await browser.new_context()
                page = await context.new_page()
                worker = asyncio.create_task(self._worker(page, i))
                workers.append(worker)
            
            # Wait for all tasks to complete
            await self.queue.join()
            
            # Cancel all workers
            for worker in workers:
                worker.cancel()
                
            # Wait for all worker tasks to be cancelled
            await asyncio.gather(*workers, return_exceptions=True)
            
            for context in [w._context for w in workers if hasattr(w, '_context')]:
                try:
                    await context.close()
                except:
                    pass
                
            await browser.close()
        
        if self.debug:
            elapsed = time.time() - start_time
            print(f"Crawling completed in {elapsed:.2f} seconds")
            print(f"Found {len(self.all_links)} links")
            print(f"Filtered out {self.positive_filtered_count} URLs (didn't match positive filters)")
            print(f"Filtered out {self.negative_filtered_count} URLs (matched negative filters)")
            
        return list(self.all_links)
    
    def _remove_fragment(self, url):
        """
        Remove the fragment part of a URL.
        
        Args:
            url (str): URL with or without fragment
            
        Returns:
            str: URL without fragment
        """
        parsed = urlparse(url)
        # Rebuild URL without fragment
        base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if parsed.query:
            base_url += f"?{parsed.query}"
        return base_url
    
    async def _worker(self, page, worker_id):
        """
        Worker to process URLs from the queue.
        
        Args:
            page: Playwright page object
            worker_id: ID of this worker for debugging
        """
        # Store context for cleanup
        setattr(page, '_context', page.context)
        
        while True:
            # Get an URL from the queue
            url = await self.queue.get()
            
            try:
                if self.debug:
                    print(f"Worker {worker_id} processing: {url}")
                
                # Get the URL without fragment for checking if page was already visited
                url_without_fragment = self._remove_fragment(url)
                
                # Skip if already visited or not part of the same domain
                if (url in self.visited_urls or 
                    url_without_fragment in self.visited_pages or 
                    urlparse(url).netloc != self.domain):
                    self.queue.task_done()
                    continue
                
                # Apply filters
                if not self._url_passes_filters(url):
                    if self.debug:
                        print(f"Worker {worker_id} skipping (filtered): {url}")
                    self.queue.task_done()
                    continue
                
                self.visited_urls.add(url)
                self.visited_pages.add(url_without_fragment)
                
                # Navigate to the page
                try:
                    await page.goto(url, wait_until="networkidle", timeout=30000)
                except Exception as e:
                    if self.debug:
                        print(f"Worker {worker_id} navigation error: {url} - {e}")
                    self.queue.task_done()
                    continue
                
                # Get all links on the page
                links = await page.evaluate('''() => {
                    const anchors = Array.from(document.querySelectorAll('a'));
                    
                    // Get links from regular anchor tags
                    const hrefLinks = anchors
                        .map(a => a.href)
                        .filter(href => href && !href.startsWith('javascript:') && !href.startsWith('#'));
                    
                    // Also look for links that might be in data attributes or other non-standard places
                    const dataLinks = [];
                    const allElements = document.querySelectorAll('*');
                    for (const el of allElements) {
                        for (const attr of el.attributes) {
                            if (attr.name.includes('href') || attr.name.includes('link') || attr.name.includes('url')) {
                                const value = attr.value;
                                if (value && 
                                    typeof value === 'string' && 
                                    !value.startsWith('javascript:') && 
                                    !value.startsWith('#') &&
                                    (value.startsWith('http') || value.startsWith('/'))
                                ) {
                                    dataLinks.push(value);
                                }
                            }
                        }
                    }
                    
                    // Find links in onclick handlers and other JavaScript attributes
                    const jsLinks = [];
                    for (const el of allElements) {
                        const onclick = el.getAttribute('onclick');
                        if (onclick) {
                            const matches = onclick.match(/['"]([^'"]*\.html|[^'"]*\.htm|[^'"]*\/)['"]|['"]([^'"]*\/[^'"]*)['"]/g);
                            if (matches) {
                                matches.forEach(match => {
                                    // Remove quotes
                                    const cleanMatch = match.replace(/['"]/g, '');
                                    if (cleanMatch) {
                                        jsLinks.push(cleanMatch);
                                    }
                                });
                            }
                        }
                    }
                    
                    return [...new Set([...hrefLinks, ...dataLinks, ...jsLinks])];
                }''')
                
                # Process and add links to the queue
                for link in links:
                    absolute_url = urljoin(url, link)
                    parsed_url = urlparse(absolute_url)
                    
                    # Skip URLs with fragments
                    if '#' in absolute_url:
                        # Add the base URL without fragment to our link collection
                        base_url = self._remove_fragment(absolute_url)
                        
                        # Only add the base URL if it's not already in our collection and it passes filters
                        if (base_url not in self.all_links and 
                            parsed_url.netloc == self.domain and 
                            base_url not in self.visited_pages and
                            self._url_passes_filters(base_url)):
                            
                            self.all_links.add(base_url)
                            await self.queue.put(base_url)
                    else:
                        # Only process links from the same domain and not yet visited
                        if (parsed_url.netloc == self.domain and 
                            absolute_url not in self.visited_urls and 
                            absolute_url not in self.visited_pages and
                            self._url_passes_filters(absolute_url)):
                            
                            # Add to all_links
                            self.all_links.add(absolute_url)
                            
                            # Add to queue for processing
                            await self.queue.put(absolute_url)
            
            except Exception as e:
                if self.debug:
                    print(f"Error processing {url}: {e}")
            
            finally:
                # Mark the task as done
                self.queue.task_done()


def main():
    """Example usage of the InsiteScraper class"""
    async def run():
        # Example with filters
        positive_filters = ['/api/', '/guide/']  # Only include URLs containing '/api/' or '/guide/'
        negative_filters = ['deprecated', re.compile(r'legacy|old')]  # Skip URLs containing 'deprecated', 'legacy', or 'old'
        
        scraper = InsiteScraper(
            "https://example.com",
            max_concurrent=5,
            debug=True,
            positive_filters=positive_filters,
            negative_filters=negative_filters
        )
        
        links = await scraper()
        print(f"Found {len(links)} links:")
        for link in sorted(links)[:10]:  # Show first 10 links
            print(f"  - {link}")
    
    asyncio.run(run())


if __name__ == "__main__":
    main() 