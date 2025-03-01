import re 
import csv
import os


def extract_youtube_id(url):
    # Regular expression pattern to match YouTube video IDs
    pattern = r'[?&]v=([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)
    else:
        return None


# Read the CSV file
csv_file_path = '/Users/lenaposhni/Documents/Healthcare Finance Project/Excel Sheet of Terms.csv'

# Open file  

with open(csv_file_path) as file_obj: 
    count = 0 
    reader_obj = csv.reader(file_obj)
    for row in reader_obj:
        if count < 2: 
            print('row', row)
            term = row[0]
            links = row[2:]
            print("LINKS", links)
            for i in range(len(links)):
                print("Curr Link", links[i]) 
                if 'youtube.com' in links[i]: 
                    video_id = extract_youtube_id(links[i])
        count += 1