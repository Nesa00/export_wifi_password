# Wi-Fi password extractor
   
This Python script retrieves WiFi profiles and passwords stored on your system and allows you to export them to a file.

⚠️ Important Note:

This script retrieves passwords stored on your system. Use it responsibly and only on devices you have permission to access.
This script is currently a work in progress (WIP). Some functionalities may not be implemented yet (e.g., exporting as CSV).
Features:

Retrieves WiFi profiles and passwords.
Exports retrieved information to a file (TXT, JSON, or XML formats are currently supported).
Provides options to show detailed information or a summary.


## Requirements:
Python 3

## Usage:

Run the script using python WWPE.py [options].
### Available options:
```
-h, --help: Show this help message and exit.
-g, --get: Retrieves WiFi profiles and passwords (required).
-e, --export: Exports retrieved information to a file (optional).
-p, --path: Specify the path for the export file (optional, defaults to "export.txt").
-d, --detail: Export detailed information (optional).
```

## Examples:

### This retrieves WiFi profiles and passwords and shows a summary.
```
python wifi_password_retriever.py -g
```

### This retrieves WiFi profiles and passwords and exports them to "export.txt" (summary).
```
python wifi_password_retriever.py -g -e
```

### This retrieves WiFi profiles and passwords, exports them with detailed information to "export.json".
```
python wifi_password_retriever.py -g -e -d -p export.json
```

#### Disclaimer:

> This script is designed for educational purposes only. 
> It demonstrates how to retrieve WiFi profiles and passwords stored on a system. 
> It should not be used on devices you don't have permission to access, as this could be a privacy violation.

Use this script wisely and have some fun exploring!
