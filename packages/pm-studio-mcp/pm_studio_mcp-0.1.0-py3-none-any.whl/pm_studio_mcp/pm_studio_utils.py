"""
Utility functions for the PM Studio MCP server.
"""
import os
import csv
import re
import glob
from .pm_studio_constant import (
    STOP_WORDS
)

def replace_stop_words(text: str) -> str:
    """Replace stop words with asterisks."""
    if not text:
        return text
    
    result = text
    for word in STOP_WORDS:
        pattern = r'\b' + word + r'\b'
        result = re.sub(pattern, '***', result, flags=re.IGNORECASE)
    
    return result

def write_csv_data(input_data, output_file, column_transform_func=None):
    """Write data to a CSV file."""
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        
        if isinstance(input_data, str) and os.path.exists(input_data):
            with open(input_data, 'r', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                for row in reader:
                    if column_transform_func:
                        row = column_transform_func(row)
                    writer.writerow(row)
        elif isinstance(input_data, list):
            for row in input_data:
                if column_transform_func:
                    row = column_transform_func(row)
                writer.writerow(row)
    
    return output_file

def find_files_by_pattern(pattern, directory):
    """Find files matching a pattern."""
    return glob.glob(os.path.join(directory, pattern))

def parse_csv_content(content):
    """Parse CSV content into rows."""
    if content.startswith('"'):
        content = content[1:]
    if content.endswith('"'):
        content = content[:-1]
    
    lines = content.split('\n')
    rows = [line.split(',') for line in lines]
    
    return rows