# AI-Powered Bookmark Categorizer

## Overview

The **AI-Powered Bookmark Categorizer** leverages cutting-edge AI using **llama3:latest** to intelligently organize your bookmarks. It analyzes each bookmark’s title and URL to recommend relevant categories such as **English, Exercise, Coding, Personal, Travel**, and more. This tool helps you keep your bookmarks organized without needing manual intervention.

## Features

- **AI-Driven Categorization**: Uses the **llama3:latest** model to suggest the most relevant categories based on the content of your bookmarks.
- **Batch Processing** *(Coming Soon)*: Allows for processing large collections of bookmarks at once.
- **ChatGPT Integration** *(Coming Soon)*: Users can input their own categories, and ChatGPT will categorize the bookmarks accordingly.
- **Custom Categories** *(Coming Soon)*: Define your own categories and have AI sort your bookmarks.

## Requirements

- Python 3.x
- Necessary Python packages (detailed below)

## Installation and Setup

Follow these steps to install and use the **AI-Powered Bookmark Categorizer**:

1. **Export your bookmarks** from your browser:
   - In your browser (Chrome, Firefox, etc.), export your bookmarks as an HTML file.
   
2. **Clone the repository** or download the `AI-Powered-Bookmark-Categorizer.py` script.

3. **Install the required Python packages** by running the following command in your terminal:

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the script** in your terminal:

    ```bash
    python3 AI-Powered-Bookmark-Categorizer.py
    ```

5. **Enter the path to your exported bookmarks**:
    - You will be prompted to input the file path for your exported bookmarks HTML file.
    
6. **Enter the output path for the categorized bookmarks**:
    - You will also be prompted to input the path for the output file, where the categorized bookmarks will be saved.

## Example Usage

```bash
$ python3 AI-Powered-Bookmark-Categorizer.py
Enter the path to your bookmarks file: bookmarks_9_26_24.html
Enter the output path for the categorized bookmarks: exported_bookmarks.html
