import googleapiclient.discovery
import os
from pytube import YouTube
id = input("Enter your playlist id: ")
id = id[id.index("list=") + 5: id.index("list=") + 39]
api_key = 'AIzaSyCL0n22RuQSq1vXZ5-T9_YJnkWARh_0n-4'
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

des = os.getcwd() + "\playlist"
i = 0
while os.path.exists(des):
    des = des + str(i)
    i += 1
def get_videos(id):
    youtube_ids = []
    request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId = id
        )

    response = request.execute()
    total = response['pageInfo']['totalResults']
    perpage = response['pageInfo']['resultsPerPage']
    count = perpage
    if total < 5:
        for i in range(total):
            youtube_ids.append(response['items'][i]['contentDetails']['videoId'])
    else:
        for i in range(perpage):
            youtube_ids.append(response['items'][i]['contentDetails']['videoId'])
        if total != perpage:
            next = response['nextPageToken']
            for i in range(total//perpage):
                request = youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId = id,
                    pageToken = next
                    )
                response = request.execute()
                for i in range(perpage):
                    count += 1
                    youtube_ids.append(response['items'][i]['contentDetails']['videoId'])
                    if count == total:
                        break
                if count == total:
                    break
                next = response['nextPageToken']
    return youtube_ids
def download():
    youtube_ids = get_videos(id)
    for i in range(len(youtube_ids)):
        try:
            url = YouTube("youtube.com/watch?v=" + youtube_ids[i])
            video = url.streams.filter(only_audio=True).first()
            out_file = video.download(output_path=des)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
        except:
            print("I found something illegal here " + youtube_ids[i])

download()