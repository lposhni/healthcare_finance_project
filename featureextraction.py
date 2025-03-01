def extract_features(response, subscriber_count):
    # Initialize default values
    duration = 'n/a'
    published_at = 'n/a'
    like_count = 'n/a'
    dislike_count = 'n/a'
    view_count = 'n/a'

    # Loop through items in the response
    for item in response.get('items', []):
        # Duration value
        duration = item.get('contentDetails', {}).get('duration', 'n/a')
        #print('Duration:', duration)

        # Channel title 
        title = item.get('snippet', {}).get('channelTitle', 'n/a')
        #print('Channel Title:', title)

        # Video Title 
        video_title = item.get('snippet', {}).get('title', 'n/a')
        #print("Video Title:", video_title)


        # Published value
        published_at = item.get('snippet', {}).get('publishedAt', 'n/a')
        #print('Published At:', published_at)

        # Like Count
        like_count = item.get('statistics', {}).get('likeCount', 'n/a')
        #print('Like Count:', like_count)

        # Dislike Count
        dislike_count = item.get('statistics', {}).get('dislikeCount', 'n/a')
        #print('Dislike Count:', dislike_count)

        # View Count
        view_count = item.get('statistics', {}).get('viewCount', 'n/a')
        #print('View Count:', view_count)

        # Language 
        language = item.get('snippet', {}).get('defaultAudioLanguage', 'n/a')
        #print("Language:", language)

    return duration, title, video_title, published_at, like_count, dislike_count, view_count, language, subscriber_count
