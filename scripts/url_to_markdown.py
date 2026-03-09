#!/usr/bin/env python3
import sys
import argparse
import json
import urllib.request
import urllib.error

def convert_url_to_markdown(url, method="auto", retain_images=False):
    """
    Convert a URL to Markdown using the markdown.new API.
    
    Args:
        url (str): The URL to convert.
        method (str): Conversion method ('auto', 'ai', 'browser'). Default 'auto'.
        retain_images (bool): Whether to retain images in the markdown. Default False.
        
    Returns:
        str: The converted markdown content.
    """
    api_url = "https://markdown.new/"
    
    # Prepare the payload
    payload = {
        "url": url,
        "method": method,
        "retain_images": retain_images
    }
    
    data = json.dumps(payload).encode('utf-8')
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    req = urllib.request.Request(api_url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

def convert_url_to_markdown_jina(url):
    """
    Convert a URL to Markdown using the Jina Reader API as a fallback.
    
    Args:
        url (str): The URL to convert.
        
    Returns:
        str: The converted markdown content.
    """
    jina_url = f"https://r.jina.ai/{url}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    req = urllib.request.Request(jina_url, headers=headers, method='GET')
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print(f"Jina HTTP Error: {e.code} - {e.reason}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"Jina URL Error: {e.reason}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Jina Error: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description='Convert URL to Markdown using markdown.new API (with Jina fallback).')
    parser.add_argument('url', help='The URL to convert')
    parser.add_argument('--method', choices=['auto', 'ai', 'browser'], default='auto',
                        help='Conversion method for markdown.new (default: auto)')
    parser.add_argument('--retain-images', action='store_true',
                        help='Retain images in the output markdown')
    
    args = parser.parse_args()
    
    # Try Jina first
    markdown = convert_url_to_markdown_jina(args.url)
    
    # Fallback to markdown.new if Jina fails
    if not markdown:
        print("Jina failed, switching to markdown.new...", file=sys.stderr)
        markdown = convert_url_to_markdown(args.url, args.method, args.retain_images)
    
    if markdown:
        print(markdown)
    else:
        print("Both markdown.new and Jina Reader failed to convert the URL.", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
