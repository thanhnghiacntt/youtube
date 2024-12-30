import googleapiclient.discovery
import csv

def get_playlist_videos(api_key, playlist_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    videos = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response.get("items", []):
            video_id = item["contentDetails"]["videoId"]
            videos.append(video_id)

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return videos

def get_video_details(api_key, video_ids):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    video_details = []
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute()

        for item in response.get("items", []):
            video_details.append({
                "title": item["snippet"]["title"],
                "url": f'https://www.youtube.com/watch?v={item["id"]}',
                "likes": item["statistics"].get("likeCount", "0"),
                "views": item["statistics"].get("viewCount", "0")
            })

    return video_details

def export_to_csv(video_details, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "URL", "Likes", "Views"])
        for video in video_details:
            writer.writerow([video["title"], video["url"], video["likes"], video["views"]])

def main():
    api_key = "AIzaSyB3UZNaDuZ_h-_GFplk7VMjfumc1vx0djk"  # Thay bằng API Key của bạn
    playlist_id = "PLjgkuGdjdz7u_pe6bxhA1wwY6RbvN_map"  # Playlist ID từ URL

    print("Fetching videos from playlist...")
    video_ids = get_playlist_videos(api_key, playlist_id)

    print("Fetching video details...")
    video_details = get_video_details(api_key, video_ids)

    output_file = "playlist_details.csv"
    print(f"Exporting data to {output_file}...")
    export_to_csv(video_details, output_file)

    print("Export completed.")

if __name__ == "__main__":
    main()
