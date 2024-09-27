import requests
from bs4 import BeautifulSoup
import ollama
from collections import defaultdict
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize Ollama client
client = ollama.Client()

def read_bookmarks(file_path):
    print("Reading bookmarks from file...")
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Extract URLs, titles, and icons
    bookmarks = []
    for link in soup.find_all('a'):
        title = link.get_text()
        url = link.get('href')
        icon = link.get('icon')  # Check for icon attribute if it exists
        if url:
            bookmarks.append({'title': title, 'url': url, 'icon': icon})
    print(f"Found {len(bookmarks)} bookmarks.")
    return bookmarks

def remove_duplicates(bookmarks):
    print("Removing duplicate bookmarks...")
    seen_urls = set()
    unique_bookmarks = []
    for bookmark in bookmarks:
        if bookmark['url'] not in seen_urls:
            unique_bookmarks.append(bookmark)
            seen_urls.add(bookmark['url'])
    print(f"Unique bookmarks: {len(unique_bookmarks)}")
    return unique_bookmarks

def check_url_status(bookmark):
    # Validate URL before categorizing
    try:
        response = requests.get(bookmark['url'], timeout=5)
        if response.status_code != 404:
            print(f"Valid URL: {bookmark['url']} - Title: {bookmark['title']}")
            return bookmark
        else:
            print(f"Invalid URL (404): {bookmark['url']} - Title: {bookmark['title']}")
    except requests.exceptions.RequestException:
        print(f"Request failed for URL: {bookmark['url']} - Title: {bookmark['title']}")
    return None

def categorize_bookmark(bookmark):
    prompt = (
        f"You are a bookmark categorizer. Based on the provided title and URL, recommend "
        f"relevant categories for this bookmark. Example categories include English, "
        f"Exercise, Coding, Personal, and Travel, but feel free to suggest others that "
        f"better fit the content. Please make sure that the category name is one word. "
        f"Only return the category name.\n\nTitle: {bookmark['title']}\nURL: {bookmark['url']}\nCategory:"
    )
    
    response = client.generate(model="llama3:latest", prompt=prompt)
    
    # Ensure you correctly extract the category from the response
    if response.get('done'):
        category = response.get('response', '').strip()
        print(f"Categorized '{bookmark['title']}' under '{category}'")
        return category
    else:
        print(f"Failed to categorize bookmark '{bookmark['title']}': {response}")
        return "Uncategorized"  # Default fallback category

def organize_bookmarks(bookmarks):
    print("Organizing bookmarks into categories...")
    categorized_bookmarks = defaultdict(list)
    
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(categorize_bookmark, bookmark): bookmark for bookmark in bookmarks}
        
        for future in as_completed(futures):
            bookmark = futures[future]
            try:
                category = future.result()
                categorized_bookmarks[category].append(bookmark)
                print(f"Categorized '{bookmark['title']}' under '{category}'")
            except Exception as e:
                print(f"Error categorizing bookmark '{bookmark['title']}': {e}")
    
    return categorized_bookmarks

def export_to_html(categorized_bookmarks, output_file):
    print(f"Exporting categorized bookmarks to {output_file}...")
    html_content = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>\n"""

    timestamp = int(datetime.now().timestamp())

    for category, bookmarks in categorized_bookmarks.items():
        html_content += f'    <DT><H3 ADD_DATE="{timestamp}" LAST_MODIFIED="{timestamp}">{category}</H3>\n'
        html_content += '    <DL><p>\n'
        for bookmark in bookmarks:
            title = bookmark['title']
            url = bookmark['url']
            icon = bookmark['icon'] if bookmark['icon'] else ""
            icon_attr = f' ICON="{icon}"' if icon else ""
            html_content += f'        <DT><A HREF="{url}" ADD_DATE="{timestamp}"{icon_attr}>{title}</A>\n'
        html_content += '    </DL><p>\n'  # Close the inner DL for each category
    
    # Close the main DL tag for bookmarks
    html_content += "</DL><p>\n"
    html_content += "</DL>"

    # Write the HTML content to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)
    print("Export completed.")

# Main function to orchestrate the bookmark processing
def main(input_file, output_file):
    bookmarks = read_bookmarks(input_file)
    unique_bookmarks = remove_duplicates(bookmarks)
    
    # Check URLs in parallel
    print("Checking URL statuses in parallel...")
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(check_url_status, bookmark): bookmark for bookmark in unique_bookmarks}
        valid_bookmarks = [future.result() for future in as_completed(futures) if future.result() is not None]
    
    print(f"Valid bookmarks: {len(valid_bookmarks)}")
    categorized_bookmarks = organize_bookmarks(valid_bookmarks)
    export_to_html(categorized_bookmarks, output_file)

# Example usage
if __name__ == "__main__":
    input_file = input("Enter the path to your input bookmarks file: ")
    output_file = input("Enter the path for the output Netscape Bookmark file: ")
    main(input_file, output_file)
