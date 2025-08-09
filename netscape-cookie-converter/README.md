# Netscape Cookie Converter

## Introduction
A Python module designed to convert JSON cookie format to Netscape cookie format. This utility provides functionality to transform browser cookie data between different formats for compatibility with various web scraping and automation tools.

## Features
- JSON to Netscape Conversion: Converts cookies from JSON format to Netscape cookie format.
- Multi-threaded Processing: Handles multiple cookie files simultaneously.
- Automated Directory Management: Creates necessary directories for organized file processing.
- Standard Cookie Format Compliance: Generates properly formatted Netscape cookies compatible with web automation tools.

## Functionality
The module includes two main functions:

1. convert_cookies(json_cookies_file, netscape_cookies_file) - Converts a single JSON cookie file to Netscape format.
2. files_processing(files) - Processes multiple files and creates corresponding Netscape cookie files.

## Usage:
```python
# Convert individual cookie file
convert_cookies('cookies.json', 'netscape_cookies.txt')

# Process all files in current directory
files = listdir('.')
files_processing(files)
```

## Output Format
The Netscape cookie format follows the standard cookie file structure:

- **domain**: Cookie domain
- **flag**: HTTPOnly flag (TRUE/FALSE)
- **path**: Cookie path
- **secure**: Secure flag (TRUE/FALSE)
- **expiry**: Expiration timestamp
- **name**: Cookie name
- **value**: Cookie value

## Dependencies
- Python 3.x
- Standard library modules: json, os, os.path

## Use Cases
This module is particularly useful for:

- Web scraping automation.
- Browser automation tools requiring Netscape cookie format.
- Cookie management in web applications.
- Data migration between different cookie storage formats.

## Files Created.
The script automatically creates two directories:

- jsons/ - For processed JSON files
- netscape/ - For converted Netscape cookie files

## Summary

This tool streamlines the process of converting browser cookies for use with various web automation frameworks and scraping tools.


