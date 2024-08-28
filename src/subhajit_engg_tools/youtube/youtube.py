# Author: Subhajit Maji
# subhajitsr@gmail.com
# +65-98302027
# Date: 2024-08-08

from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import Any, Optional, Dict, List
import json
import datetime
import logging


class CredentialError(Exception):
    """This exception is raised when there is error in creating credential."""

class YoutubeDataError(Exception):
    """This exception is raised when there is error in creating Youtube data object."""

class InsufficientInputError(Exception):
    """This exception is raised when insufficint info is provided to create channel object."""

class ChannelNotFoundError(Exception):
    """This exception is raised when a channel is not found."""

class YoutubeChannel():
    def __init__(self,
                 service_account_info: json,
                 scopes: Optional[list] = ['https://www.googleapis.com/auth/youtube.readonly'],
                 channel_name: Optional[str] = None,
                channel_id: Optional[str] = None) -> None:
        # Trying to create the credential object
        try:
            credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=scopes
            )
        except Exception as e:
            raise CredentialError(e)
        
        # Trying to build the youtube object
        try:
            youtube = build('youtube', 'v3', credentials=credentials)
        except Exception as e:
            raise YoutubeDataError(e)
            
        # Fetching Channel id by name
        if channel_name is None and channel_id is None:
            raise InsufficientInputError("Either channel_name or channel_id needs to be provided")
        
        if channel_id is None:
            # Fetch channel ID by name
            response = youtube.search().list(q=channel_name, type='channel', part='id', maxResults=1).execute()
            if not response.get('items'):
                raise ChannelNotFoundError(f"No channel found for username: {channel_name}")
            channel_id = response['items'][0]['id']['channelId']
        else:
            # Verify the channel id passed is correct
            if not youtube.channels().list(id=channel_id,part='id').execute().get('items'):
                raise ChannelNotFoundError(f"No channel found for channel_id: {channel_id}")
        
        # Get channel attributes
        response = youtube.channels().list(
            id=channel_id,
            part='snippet,statistics'
        ).execute()
        
        # Set Channel attribute for the object
        self._credentials = credentials
        self._youtube = youtube
        self.channel_name = channel_name
        self.channel_id = channel_id
        self.title = response.get('items')[0].get('snippet').get('title')
        self.description = response.get('items')[0].get('snippet').get('description')
        self.customUrl = response.get('items')[0].get('snippet').get('customUrl')
        self.publishedAt = response.get('items')[0].get('snippet').get('publishedAt')
        self.country = response.get('items')[0].get('snippet').get('country')
        self.viewCount = response.get('items')[0].get('statistics').get('viewCount')
        self.subscriberCount = response.get('items')[0].get('statistics').get('subscriberCount')
        self.videoCount = response.get('items')[0].get('statistics').get('videoCount')
    
    @staticmethod
    def get_video_statistics(youtube: Any, video_ids: list) -> list:
        video_stats = []

        # Fetch statistics for the videos
        video_response = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(video_ids)
        ).execute()

        for item in video_response['items']:
            video_stats.append({
                'id': item['id'],
                'title': item['snippet']['title'],
                'url': f"https://www.youtube.com/watch?v={item['id']}",
                'views': item['statistics'].get('viewCount',0),
                'likes': item['statistics'].get('likeCount',0),
                'dislikes': item['statistics'].get('dislikeCount',0),
                'comments': item['statistics'].get('commentCount', 0),
                'publishedAt': item['snippet']['publishedAt']
            })
    
        return video_stats

    
    def get_video_data(self, chunk_size: Optional[int] = 50, days_count: Optional[int] = 365):
        video_data = []
        
        # Calculating published_after based on days_count
        t_ago = datetime.datetime.now() - datetime.timedelta(days=days_count)
        published_after = t_ago.isoformat("T") + "Z"

        request = self._youtube.search().list(
                    part='id',
                    channelId=self.channel_id,
                    publishedAfter=published_after,
                    maxResults=chunk_size,
                    type='video'
                )

        while request:
            response = request.execute()
            video_ids = [item['id']['videoId'] for item in response['items']]
            
            # Getting video statistics
            video_data = video_data + self.get_video_statistics(self._youtube, video_ids)
            
            # Creating request for the next chunk fetch
            request = self._youtube.search().list_next(request, response)        
                
        return video_data
