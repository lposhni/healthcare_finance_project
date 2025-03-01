

# -*- coding: utf-8 -*-

import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import re 
import csv
import os
import datetime
from collections import namedtuple
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from featureextraction import extract_features

from pprint import pprint
from Google import create_service
from comment_extraction import create_comment_csv

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube']
api_key = 'AIzaSyD4vI6wl181RvvD7F1jiLp4I2wnj8xXxqk' 
service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)









# Define the pattern to identify and capture YouTube video IDs
youtube_pattern = re.compile(r'https://www\.youtube\.com/watch\?v=([a-zA-Z0-9_-]+)')

def extract_youtube_id(url):
    # Regular expression pattern to match YouTube video IDs
    pattern = r'[?&]v=([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None
    
def get_youtube_video_id(url):
    # Define a regex pattern to match YouTube Shorts URLs
    pattern = r'https://www\.youtube\.com/shorts/([a-zA-Z0-9_-]+)'
    
    # Search for the video ID using the regex pattern
    match = re.search(pattern, url)
    
    # Return the video ID if found, otherwise return None
    if match:
        return match.group(1)
    else:
        return None

def get_subscriber_count(response):
    try:
        # Extract channelId from the response
        channel_id = response['items'][0]['snippet']['channelId']
        
        # Define the parts to request
        part_string = 'contentDetails,statistics,snippet'
        
        # Make the API request to get channel details
        response = service.channels().list(
            part=part_string,
            id=channel_id
        ).execute()
        
        # Check if items are present in the response
        if not response.get('items'):
            return 'n/a'
        
        # Get the statistics part
        statistics = response['items'][0].get('statistics', {})
        
        # Return the subscriber count or 'n/a' if not available
        return statistics.get('subscriberCount', 'n/a')
    
    except (KeyError, IndexError) as e:
        # Handle cases where the response format is not as expected
        return 'n/a'
    except Exception as e:
        # Handle other exceptions, if necessary
        print(f"An error occurred: {e}")
        return 'n/a'


def get_descriptive_details(response): 
    tags = 'n/a'
    description = 'n/a'

    for item in response.get('items', []):
        # Duration value
        description = item.get('snippet', {}).get('description', 'n/a')
        #print('Duration:', duration)

        # Channel title 
        tags = item.get('snippet', {}).get('tags', 'n/a')
        #print('Channel Title:', title)

    return tags, description 
    



# Read the CSV file
csv_file_path = '/Users/lenaposhni/Documents/Healthcare Finance Project/Excel Sheet of Terms1.csv'

# Make new output CSV
filename = "output1.csv"
headers = ["term", "video_id", "duration", "publisher", "video_title", "published_at", "like_count", "dislike_count", "view_count", "language", "subscriber count"]
res_list = []
description_list = []
csv_file = 'comments_data1.csv'  # Name your file
descriptive_csv_file = 'descriptive_file1.csv'


# Open file  
with open(csv_file_path) as file_obj: 
    reader_obj = csv.reader(file_obj)
    for row in reader_obj:
        #if count < 2: 
        term = row[0]
        links = row[2:]
        
        # loops through each row 
        for i in range(len(links)):
            print(links)
            if 'shorts' in links[i]: 
                video_id = get_youtube_video_id(links[i]) 
                part_string = 'contentDetails,statistics,snippet'
                response = service.videos().list(part=part_string,id=video_id).execute()
                
                # features 
                subscriber_count = get_subscriber_count(response)
                duration, title, video_title, published_at, like_count, dislike_count, view_count, language, subscriber_count = extract_features(response, subscriber_count)
                res_list.append((term, video_id, duration, title, video_title, published_at, like_count, dislike_count, view_count, language, subscriber_count))
                
                # descriptive details 
                tags, description = get_descriptive_details(response)
                description_list.append((video_id, tags, description))

            elif links[i] == '': 
                continue 

            else: 
                video_id = extract_youtube_id(links[i])
                part_string = 'contentDetails,statistics,snippet'
                response = service.videos().list(part=part_string,id=video_id).execute()

                # features 
                subscriber_count = get_subscriber_count(response)
                duration, title, video_title, published_at, like_count, dislike_count, view_count, language, subscriber_count = extract_features(response, subscriber_count)
                res_list.append((term, video_id, duration, title, video_title, published_at, like_count, dislike_count, view_count, language, subscriber_count))

                # descriptive details 
                tags, description = get_descriptive_details(response)
                description_list.append((video_id, tags, description))

            create_comment_csv(video_id, csv_file)





# Write data to CSV
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # Write the header
    writer.writerows(res_list)  # Write the data rows

print(f"Data successfully written to {filename}")


with open(descriptive_csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['video_id', 'tags', 'description'])  # Write the header
    writer.writerows(description_list)  # Write the data rows
            
print(f"Data successfully written to {descriptive_csv_file}")


              
	



