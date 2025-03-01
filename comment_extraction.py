import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
from googleapiclient.discovery import build
import os
import pandas as pd
from googleapiclient.errors import HttpError
import csv


# Initialize the YouTube API client
api_key = 'AIzaSyD4vI6wl181RvvD7F1jiLp4I2wnj8xXxqk'
youtube = build('youtube', 'v3', developerKey=api_key)

def get_replies(youtube, parent_id, video_id):
    replies = []
    next_page_token = None
    while True:
        reply_request = youtube.comments().list(
            part="snippet",
            parentId=parent_id,
            textFormat="plainText",
            maxResults=25,
            pageToken=next_page_token
        )
        reply_response = reply_request.execute()
        for item in reply_response['items']:
            comment = item['snippet']
            replies.append({
                'Timestamp': comment['publishedAt'],
                'Username': comment['authorDisplayName'],
                'VideoID': video_id,
                'Comment': comment['textDisplay'],
                'Date': comment['updatedAt'] if 'updatedAt' in comment else comment['publishedAt']
            })
        next_page_token = reply_response.get('nextPageToken')
        if not next_page_token:
            break
    return replies



def get_comments_for_video(youtube, video_id, max_comments=100, csv_filename='comments_log.csv'):
    all_comments = []
    next_page_token = None
    comments_count = 0
    if comments_count >= max_comments: 
        return all_comments
    try:
        while comments_count < max_comments:
            comment_request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=next_page_token,
                textFormat="plainText",
                maxResults=100 # is this randomized 
            )
            comment_response = comment_request.execute()
            for item in comment_response['items']:
                if comments_count >= max_comments:
                    return all_comments

                top_comment = item['snippet']['topLevelComment']['snippet']
                replies_for_one_comment = []

                # Fetch replies if there are any
                if item['snippet']['totalReplyCount'] > 0:
                    total_replies = get_replies(youtube, item['snippet']['topLevelComment']['id'], video_id)
                    for entry in total_replies:
                        reply_comment = entry['Comment']
                        replies_for_one_comment.append(reply_comment)

                if len(replies_for_one_comment) > 4:
                    replies_for_one_comment = replies_for_one_comment[:5]

                all_comments.append({
                    'VideoID': video_id,
                    #'Timestamp': top_comment['publishedAt'],
                    'Username': top_comment['authorDisplayName'],
                    'Comment': top_comment['textDisplay'],
                    #'Date': top_comment['updatedAt'] if 'updatedAt' in top_comment else top_comment['publishedAt'],
                    'TotalReplies': item['snippet']['totalReplyCount'],
                    'Replies': replies_for_one_comment
                })

                comments_count += 1

            next_page_token = comment_response.get('nextPageToken')
            if not next_page_token: 
                break


    except HttpError as e:
        if e.resp.status == 403 and 'commentsDisabled' in str(e):
            # Handle the case where comments are disabled
            # Add a row to the all_comments list indicating comments are disabled
            all_comments.append({
                'VideoID': video_id,
                'Username': 'disabled',
                'Comment': 'disabled',
                'TotalReplies': 'disabled',
                'Replies': ['disabled']
            })
            return all_comments
    return all_comments


def create_comment_csv(video_id, csv_file):
    all_comments = []
    # Collect comments
    video_comments = get_comments_for_video(youtube, video_id)
    all_comments.extend(video_comments)
    # Create DataFrame
    comments_df = pd.DataFrame(all_comments)
    # Check if the file exists
    file_exists = os.path.isfile(csv_file)
    # Append to the CSV file if it exists, otherwise write a new file with header
    comments_df.to_csv(csv_file, mode='a', header=not file_exists, index=False)
    return csv_file




#video_id = 'cgHBfcO8f8I'
#create_comment_csv(video_id, 'comment_ex_csv.csv')




















'''
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

request = youtube.commentThreads().list(
    part="snippet",
    videoId="I79UaXHPZDo",
    maxResults=100
)
response = request.execute()

comments = []
for item in response['items']:
    print("Item", item)
    print("       ")


    comment = item['snippet']['topLevelComment']['snippet']
    comments.append([
        comment['authorDisplayName'],
        comment['publishedAt'],
        comment['updatedAt'],
        comment['likeCount'],
        comment['textDisplay'],
        item['snippet']['totalReplyCount'],

    ])

df = pd.DataFrame(comments, columns=['author', 'published_at', 'updated_at', 'like_count', 'text', 'total_reply_count'])

df.head(10)
print(df)
'''