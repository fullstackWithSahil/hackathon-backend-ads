youtube_api_key="AIzaSyDPbsNFVLgMRMKWr2APoPek2ZWwzShqL6E"
from googleapiclient.discovery import build

# Replace with your YouTube Data API v3 key
API_KEY = youtube_api_key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def get_video_data(query, max_results=5):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

    # Search for videos
    search_response = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=max_results,
        type="video"
    ).execute()

    video_data = []

    for item in search_response.get("items", []):
        video_id = item["id"]["videoId"]

        # Get video details (title, likes, views)
        video_details_response = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        ).execute()

        video_details = video_details_response.get("items", [])[0]
        title = video_details["snippet"]["title"]
        likes = int(video_details["statistics"].get("likeCount", 0))
        views = int(video_details["statistics"].get("viewCount", 0))

        # Get comments
        comments = []
        try:
            comment_response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,  # Adjust as needed (maximum is 100 per request)
                textFormat="plainText"
            ).execute()

            for comment in comment_response.get("items", []):
                comment_text = comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment_text)


        except Exception as e:
            print(f"Could not fetch comments for video ID {video_id}: {e}")

        # Append data in the desired format
        video_data.append({
            "title": title,
            "likes": likes,
            "comments": comments,
            "views": views,
        })

    return video_data

if __name__ == "__main__":
    query = "marketing"
    result = get_video_data(query)
    print(result)
