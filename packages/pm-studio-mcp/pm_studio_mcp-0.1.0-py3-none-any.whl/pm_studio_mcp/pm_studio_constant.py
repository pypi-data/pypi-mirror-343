"""
Constants used in the PM Studio MCP server.
"""

# File patterns
QUERY_RESULT_PATTERN = "query_result.csv"
UNWRAP_FEEDBACK_PATTERN = "Unwrap_Feedback*.csv"

# Output file names
OCV_CLEANED_FILE = "ocv_data_cleaned.csv"
UNWRAP_CLEANED_FILE = "unwrap_data_cleaned.csv"
ALL_DATA_CLEANED_FILE = "all_data_cleaned.csv"
FINAL_RESULT_FILE = "final_result.csv"

# Column indexes
OCV_COLUMN_INDEX = 38  # 39th column (0-based index)
UNWRAP_DEFAULT_COLUMN_INDEX = 2  # 3rd column (0-based index)
UNWRAP_COLUMN_NAME = "Entry Text"
OCV_COLUMN_NAME = "Issue[0].Title"  # Add this constant for OCV clean tool

# Stop words
STOP_WORDS = ['fuck', 'shit', 'damn', 'ass', 'bitch', 'crap']

# Greeting message template
GREETING_TEMPLATE = "hello, {name}! How can I help you today? I can help you to do competitor analysis, user feedback summary, write docs and more!"