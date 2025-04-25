import asyncio
import os
import mimetypes
from pathlib import Path
from urllib.parse import urlparse
from playwright.async_api import async_playwright
import time
try:
    from pypdf import PdfWriter, PdfReader
except ImportError:
    raise ImportError("pypdf library is required. Install it with: pip install pypdf")


class InsiteProcessor:
    def __init__(self, output_dir="output", max_concurrent=3, debug=False):
        """
        Initialize the InsiteProcessor.
        
        Args:
            output_dir (str): Directory where PDFs will be saved
            max_concurrent (int): Maximum number of concurrent page processing tasks
            debug (bool): Enable debug output
        """
        self.output_dir = output_dir
        self.max_concurrent = max_concurrent
        self.debug = debug
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Initialize mimetypes
        mimetypes.init()
        
        # Initialize the PDF writer
        self.Files = PdfWriter()
        
        # Keep track of all PDF files created
        self.pdf_files = []
    
    async def process_links(self, links):
        """
        Process a list of links to create PDFs.
        
        Args:
            links (list): List of URLs to process
        """
        start_time = time.time()
        pages = []
        
        # Clear any previous files
        self.Files = PdfWriter()
        self.pdf_files = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            
            try:
                # Create a semaphore to limit concurrent tasks
                semaphore = asyncio.Semaphore(self.max_concurrent)
                
                # Filter out binary files and other non-HTML content
                filtered_links = []
                skipped_links = []
                
                for link in links:
                    if self._should_process_url(link):
                        filtered_links.append(link)
                    else:
                        skipped_links.append(link)
                        if self.debug:
                            print(f"Skipping non-HTML content: {link}")
                
                if self.debug and skipped_links:
                    print(f"Skipped {len(skipped_links)} links that appear to be binary or non-HTML content")
                
                # Process links with controlled concurrency
                tasks = []
                for i, link in enumerate(filtered_links):
                    task = self._process_with_semaphore(semaphore, context, link, i, pages)
                    tasks.append(task)
                
                # Wait for all tasks to complete and gather results
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Count successes and failures
                successes = sum(1 for r in results if r is True)
                failures = sum(1 for r in results if r is not True)
                
                if self.debug:
                    elapsed = time.time() - start_time
                    print(f"PDF processing completed in {elapsed:.2f} seconds")
                    print(f"Processed {len(filtered_links)} links: {successes} successful, {failures} failed")
                
                # Add all created PDFs to the PdfWriter
                self._add_pdfs_to_writer()
                
                return successes, failures
                
            finally:
                # Make sure to close all pages
                for page in pages:
                    try:
                        await page.close()
                    except Exception:
                        pass
                
                # Properly close the browser
                try:
                    await context.close()
                except Exception:
                    pass
                
                try:
                    await browser.close()
                except Exception:
                    pass
    
    def _add_pdfs_to_writer(self):
        """
        Add all PDFs in the output directory to the PdfWriter object.
        """
        # Reset the PdfWriter
        self.Files = PdfWriter()
        self.pdf_files = []
        
        # Walk through the output directory and find all PDF files
        for root, dirs, files in os.walk(self.output_dir):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_path = os.path.join(root, file)
                    try:
                        # Add the PDF to our list of files
                        self.pdf_files.append(pdf_path)
                        
                        if self.debug:
                            print(f"Adding PDF to merger: {pdf_path}")
                        
                        # Add the PDF to the writer
                        reader = PdfReader(pdf_path)
                        for page_num in range(len(reader.pages)):
                            self.Files.add_page(reader.pages[page_num])
                            
                    except Exception as e:
                        if self.debug:
                            print(f"Error adding PDF {pdf_path} to merger: {e}")
    
    def merge_to_masterfile(self, output_path=None):
        """
        Merge all PDFs into a single master file.
        
        Args:
            output_path (str, optional): Path where the merged PDF should be saved.
                                         If None, saves to 'master.pdf' in the output directory.
        
        Returns:
            str: Path to the merged PDF file
        """
        if not self.pdf_files:
            self._add_pdfs_to_writer()
            
        if not self.pdf_files:
            print("No PDF files found to merge")
            return None
        
        # Determine the output path
        if output_path is None:
            output_path = os.path.join(self.output_dir, "master.pdf")
        
        # Create directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write the merged PDF
        try:
            with open(output_path, 'wb') as f:
                self.Files.write(f)
            
            print(f"Successfully merged {len(self.pdf_files)} PDFs into: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error merging PDFs: {e}")
            return None
    
    def _should_process_url(self, url):
        """
        Determine if a URL should be processed based on its extension and content type.
        
        Args:
            url (str): URL to check
            
        Returns:
            bool: True if the URL should be processed, False otherwise
        """
        # Skip common binary files and non-HTML content
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()
        
        # Skip if the URL has a file extension that indicates binary content
        binary_extensions = [
            '.zip', '.tar', '.gz', '.rar', '.7z',
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico',
            '.mp3', '.mp4', '.wav', '.avi', '.mov', '.wmv',
            '.exe', '.dll', '.so', '.bin', '.dat',
            '.ttf', '.woff', '.woff2', '.eot',
        ]
        
        for ext in binary_extensions:
            if path.endswith(ext):
                return False
        
        # Try to determine MIME type
        mime_type, _ = mimetypes.guess_type(url)
        if mime_type and not (mime_type.startswith('text/') or 
                             mime_type == 'application/xhtml+xml' or 
                             mime_type == 'application/xml' or
                             mime_type == 'application/json'):
            return False
        
        return True
    
    async def _process_with_semaphore(self, semaphore, context, url, task_id, pages_list):
        """
        Process a single link with semaphore control.
        
        Args:
            semaphore: Asyncio semaphore for concurrency control
            context: Playwright browser context
            url: URL to process
            task_id: Task identifier for debugging
            pages_list: List to track created pages for cleanup
        
        Returns:
            bool: True if processing was successful
        """
        async with semaphore:
            if self.debug:
                print(f"Task {task_id}: Starting processing of {url}")
            return await self._process_single_link(context, url, task_id, pages_list)
    
    async def _process_single_link(self, context, url, task_id=0, pages_list=None):
        """
        Process a single link into a PDF.
        
        Args:
            context: Playwright browser context
            url (str): URL to process
            task_id: Task identifier for debugging
            pages_list: List to track created pages for cleanup
            
        Returns:
            bool: True if processing was successful
        """
        page = None
        try:
            # Create a new page for this URL
            page = await context.new_page()
            if pages_list is not None:
                pages_list.append(page)
            
            # Increase the timeout for navigation
            page.set_default_timeout(60000)  # 60 seconds
            
            # Navigate to the page and wait for network idle to ensure images load
            try:
                response = await page.goto(url, wait_until="networkidle", timeout=60000)
                
                # If response isn't HTML, skip it
                if response and response.headers.get('content-type') and not any(
                    content_type in response.headers.get('content-type').lower() 
                    for content_type in ['text/html', 'application/xhtml', 'text/xml']
                ):
                    if self.debug:
                        print(f"Task {task_id}: Skipping non-HTML content for {url} " 
                              f"(content-type: {response.headers.get('content-type')})")
                    
                    # Don't close the page here, it's now tracked and will be closed in the finally block of process_links
                    return False
                
            except Exception as e:
                if self.debug:
                    print(f"Task {task_id}: Navigation timeout for {url}: {e}")
                # If timeout, still try to continue with what's loaded
            
            # Wait a bit more to ensure all media is loaded (including lazy-loaded images)
            await page.wait_for_timeout(2000)
            
            # Force all media elements to load by scrolling down the page
            await page.evaluate("""
                () => {
                    try {
                        // Scroll down to bottom of page to trigger lazy loading
                        window.scrollTo(0, document.body.scrollHeight);
                        
                        // Force load all images
                        const images = document.querySelectorAll('img');
                        for (const img of images) {
                            // If image has data-src attribute (common in lazy loading), set src to its value
                            if (img.getAttribute('data-src')) {
                                img.src = img.getAttribute('data-src');
                            }
                            // Make image visible if it's hidden
                            img.style.display = 'block';
                            img.style.visibility = 'visible';
                            img.style.opacity = '1';
                        }
                        
                        // Force load all iframes (which might contain embedded media)
                        const iframes = document.querySelectorAll('iframe');
                        for (const iframe of iframes) {
                            if (iframe.getAttribute('data-src')) {
                                iframe.src = iframe.getAttribute('data-src');
                            }
                        }
                        
                        // Force display of elements that might be hidden until interaction
                        const hiddenElements = document.querySelectorAll('[class*="hidden"], [style*="display: none"]');
                        for (const el of hiddenElements) {
                            if (el.classList.contains('lazy') || el.getAttribute('data-lazy')) {
                                el.style.display = 'block';
                                el.style.visibility = 'visible';
                                el.style.opacity = '1';
                            }
                        }
                        
                        // Scroll back to top
                        window.scrollTo(0, 0);
                        
                        return true;
                    } catch (e) {
                        console.error('Error processing media:', e);
                        return false;
                    }
                }
            """)
            
            # Wait a bit more after forcing media to load
            await page.wait_for_timeout(1000)
            
            # Determine the file path for the PDF based on the URL structure
            pdf_path = self._get_pdf_path_from_url(url)
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
            
            # Generate the PDF
            await page.pdf(path=pdf_path, format="A4", print_background=True)
            
            if self.debug:
                print(f"Task {task_id}: Created PDF for {url} at {pdf_path}")
            
            return True
            
        except Exception as e:
            if self.debug:
                print(f"Task {task_id}: Error processing {url}: {e}")
            return False
        
        finally:
            # Note: We don't close the page here anymore to prevent TargetClosedError
            # Pages are now tracked and closed in the finally block of process_links
            pass
    
    def _get_pdf_path_from_url(self, url):
        """
        Convert a URL to a local file path for the PDF.
        
        Args:
            url (str): URL to convert
            
        Returns:
            str: Path where the PDF should be saved
        """
        parsed_url = urlparse(url)
        
        # Extract domain as the base directory
        domain = parsed_url.netloc
        
        # Get the path and remove any trailing slashes
        path = parsed_url.path.strip('/')
        
        # Handle empty path (homepage)
        if not path:
            path = "index"
        
        # Replace file extension if it exists, otherwise add .pdf
        if path.endswith(('.html', '.htm', '.php', '.asp', '.aspx', '.jsp')):
            path = os.path.splitext(path)[0]
        
        # Create directory structure based on path components
        path_components = path.split('/')
        filename = path_components.pop() if path_components else "index"
        
        # Build the directory path
        dir_path = os.path.join(self.output_dir, domain, *path_components)
        
        # Ensure safe filenames
        filename = self._sanitize_filename(filename)
        
        # Build the full file path
        pdf_path = os.path.join(dir_path, f"{filename}.pdf")
        
        return pdf_path
    
    def _sanitize_filename(self, filename):
        """
        Sanitize a filename to ensure it's valid for the file system.
        
        Args:
            filename (str): Filename to sanitize
            
        Returns:
            str: Sanitized filename
        """
        # Replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Limit length
        if len(filename) > 200:
            filename = filename[:200]
        
        return filename


def main():
    """Example usage of the InsiteProcessor class"""
    from scraper import InsiteScraper
    
    async def run():
        # First, get links using the scraper
        scraper = InsiteScraper("https://example.com", max_concurrent=5, debug=True)
        links = await scraper()
        
        # Then process those links
        processor = InsiteProcessor(output_dir="documentation", max_concurrent=3, debug=True)
        successes, failures = await processor.process_links(links)
        print(f"Processing complete: {successes} successful, {failures} failed")
        
        # Merge PDFs into a single file
        master_pdf = processor.merge_to_masterfile()
        if master_pdf:
            print(f"Created master PDF: {master_pdf}")
    
    asyncio.run(run())


if __name__ == "__main__":
    main() 