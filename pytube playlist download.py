from pytube import Playlist
import pyperclip as p

def download_playlist(playlist_url, output_directory):
  playlist = Playlist(playlist_url)
  print(f"Playlist: {playlist.title}")

  for i, video in enumerate(playlist.videos):
    try:
      video_stream = video.streams.filter(progressive=True).order_by('resolution').desc().first()
      video_stream.download(output_path=output_directory+str(playlist.title).replace('/',' '), filename= str(i+1)+"- "+str(video.title).replace('/',' ')+".mp4")
      print(f"listo: {video.title}")
    except Exception as e:
      print(f"Error para {video.title}: {e}")

playlist_url =  p.paste() 
output_directory = "/home/USER/Vídeos/"

download_playlist(playlist_url, output_directory)