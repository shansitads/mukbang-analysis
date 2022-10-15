import pandas as pd

def get_channel_stats(youtube, channel_ids):
    all_data = []
    
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=','.join(channel_ids)
    )
    response = request.execute()
    
    # loop throught items
    for item in response['items']:
        data = {'channelName':item['snippet']['title'],
        'subscribers':item['statistics']['subscriberCount'],
        'views':item['statistics']['viewCount'],
        'totalViews':item['statistics']['videoCount'],
        'playlistId': item['contentDetails']['relatedPlaylists']['uploads']
        }
        all_data.append(data)

    return(pd.DataFrame(all_data))

def get_video_ids(youtube, playlist_id):
    video_ids = []
    
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id,
        maxResults = 50
    )
    response = request.execute()
    
    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])
    
    next_page_token = response.get('nextPageToken')
    while next_page_token is not None:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults = 50,
            pageToken = next_page_token)
        response = request.execute()
    
        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])
    
        next_page_token = response.get('nextPageToken')
    
    return video_ids

def get_video_details(youtube, video_ids):
    all_video_info = []
    
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute()

        for video in response['items']:
            stats_to_keep = {'snippet' : ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                            'statistics' : ['viewCount', 'likeCount', 'favouritecounut', 'commentCount'],
                            'contentDetails': ['duration', 'definition', 'caption']
                            }

            video_info = {}
            video_info['video_id'] = video['id']

            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None

            all_video_info.append(video_info)
    
    return pd.DataFrame(all_video_info)