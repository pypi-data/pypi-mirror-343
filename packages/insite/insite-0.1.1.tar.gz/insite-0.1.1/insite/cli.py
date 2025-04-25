#!/usr/bin/env python3
"""
Command-line interface for the InSite module.
"""

import asyncio
import argparse
import re
import sys
from .scraper import InsiteScraper
from .processor import InsiteProcessor


async def main_async(args):
    """
    Asynchronous main function that processes the command line arguments.
    
    Args:
        args: Command line arguments from argparse
    """
    print(f"Starting InSite crawler for: {args.url}")
    print("-" * 50)
    
    # Convert string positive filters to list
    positive_filters = args.positive_filters.split(',') if args.positive_filters else []
    
    # Parse and convert negative filters
    negative_filters = []
    if args.negative_filters:
        for neg_filter in args.negative_filters.split(','):
            # Check if it's a regex pattern (enclosed in //)
            if neg_filter.startswith('/') and neg_filter.endswith('/') and len(neg_filter) > 2:
                pattern = neg_filter[1:-1]  # Remove the slashes
                try:
                    regex = re.compile(pattern)
                    negative_filters.append(regex)
                except re.error:
                    print(f"Warning: Invalid regex pattern '{pattern}'. Using as literal string.")
                    negative_filters.append(pattern)
            else:
                negative_filters.append(neg_filter)
    
    # Initialize the scraper
    scraper = InsiteScraper(
        args.url,
        max_concurrent=args.workers,
        debug=args.verbose,
        positive_filters=positive_filters if positive_filters else None,
        negative_filters=negative_filters if negative_filters else None
    )
    
    # Crawl the website
    print("Crawling website for links...")
    links = await scraper()
    print(f"Found {len(links)} links")
    
    # Limit the number of pages if specified
    if args.max_pages and len(links) > args.max_pages:
        print(f"Limiting to {args.max_pages} pages as requested")
        links = links[:args.max_pages]
    
    # Process links into PDFs
    if not args.crawl_only:
        print(f"Processing {len(links)} links into PDFs...")
        processor = InsiteProcessor(
            output_dir=args.output, 
            max_concurrent=args.processors,
            debug=args.verbose
        )
        
        successes, failures = await processor.process_links(links)
        print(f"PDF processing complete: {successes} successful, {failures} failed")
        
        # Create master PDF if requested
        if args.create_master and successes > 0:
            print("Creating master PDF...")
            master_file = processor.merge_to_masterfile(args.master_path)
            
            if master_file:
                print(f"Master PDF created: {master_file}")
            else:
                print("Failed to create master PDF")
    else:
        print("Crawl-only mode: Skipping PDF generation")
    
    print("\nInSite process complete!")


def main():
    """
    Command-line entry point for the InSite module.
    """
    parser = argparse.ArgumentParser(
        description="InSite - Tool for crawling websites and creating PDFs of their pages",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument('--url', type=str, required=True,
                        help='URL of the website to crawl')
    
    parser.add_argument('--output', type=str, default='insite_output',
                        help='Directory to save PDFs to')
    
    parser.add_argument('--max-pages', type=int, default=0,
                        help='Maximum number of pages to process (0 for all)')
    
    parser.add_argument('--workers', type=int, default=5,
                        help='Number of concurrent crawling workers')
    
    parser.add_argument('--processors', type=int, default=3,
                        help='Number of concurrent PDF processors')
    
    parser.add_argument('--create-master', action='store_true',
                        help='Create a master PDF file with all pages')
    
    parser.add_argument('--master-path', type=str, default=None,
                        help='Path for the master PDF (default: output/master.pdf)')
    
    parser.add_argument('--positive-filters', type=str, default='',
                        help='Comma-separated list of strings that URLs must contain')
    
    parser.add_argument('--negative-filters', type=str, default='',
                        help='Comma-separated list of strings or regex patterns (/pattern/) that URLs must NOT contain')
    
    parser.add_argument('--crawl-only', action='store_true',
                        help='Only crawl the website, do not create PDFs')
    
    parser.add_argument('--verbose', action='store_true',
                        help='Enable verbose output')
    
    args = parser.parse_args()
    
    try:
        asyncio.run(main_async(args))
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 