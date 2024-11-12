import re
import os


def read_file_content(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def extract_emails(content):
    if content is None:
        return []
    
    # Matches email addresses:
    # - Must start with alphanumeric character
    # - Followed by one or more alphanumeric chars, dots, underscores, plus signs, or hyphens
    # - Followed by @ symbol
    # - Domain part contains alphanumeric chars, dots, and hyphens
    # - TLD must be at least 2 characters long
    email_pattern = r'[A-Za-z0-9][A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
    emails = re.findall(email_pattern, content)
    return emails

def extract_dates(content):
    if content is None:
        return []
    
    dates = []
    # Matches formats like 01/02/2021, 12-25-2020
    date_pattern1 = r'(?:0?[1-9]|1[0-2])[-/](?:0?[1-9]|[12][0-9]|3[01])[-/](?:19|20)\d{2}';
    dates.extend(re.findall(date_pattern1, content))

    # Matches formats like "March 14, 2022" and "December 25, 2020"
    date_pattern2 = r'(?:19|20)\d{2}[-./](?:0?[1-9]|1[0-2])[-./](?:0?[1-9]|[12][0-9]|3[01])';
    dates.extend(re.findall(date_pattern2, content))
    
    # Matches formats like "January 14, 2022" and "December 25, 2020"
    date_pattern3 = r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}';
    dates.extend(re.findall(date_pattern3, content))

    return dates

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'text.txt')
    
    content = read_file_content(file_path)
    if content is None:
        return
    
    emails = extract_emails(content)
    if emails:
        print("Found emails:")
        for email in emails:
            print(email)
    else:
        print("No emails found in the file.")
    
    dates = extract_dates(content)
    if dates:
        print("\nFound dates:")
        for date in dates:
            print(date)
    else:
        print("\nNo dates found in the file.")

if __name__ == "__main__":
    main()