#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import webbrowser


# Set DEVELOPER_KEY to the API key value 
DEVELOPER_KEY = "PUT_YOUR_KEY_HERE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()

  videos_id = []
  videos_title = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos_id.append(search_result["id"]["videoId"])
      videos_title.append(search_result["snippet"]["title"])
  
  i = 0
  for vid in videos_title:
    print "Videos:\n", "%s: %s"%(i+1,videos_title[i])
    i += 1

  choice = int(raw_input("Enter video number to watch: "))

  webbrowser.open("https://www.youtube.com/watch?v=%s"%(videos_id[choice-1]),new = 2)


if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--max-results", help="Max results", default=25)
  args = argparser.parse_args()

  try:
    youtube_search(args)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)


