import requests
import mutagen
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import os
import sys

def get_lyrics(artist_name, track_name, album_name, duration):
    response = requests.get(f"https://lrclib.net/api/get?artist_name={artist_name}&track_name={track_name}&album_name={album_name}&duration={duration}")
    data = response.json()

    if response.status_code == 200:
        if data["syncedLyrics"]:
            print("Synced lyrics found")
            lyrics = data["syncedLyrics"]
            return lyrics
        else:
            print("Plain lyrics found")
            lyrics = data["plainLyrics"]
            return lyrics
    if response.status_code == 404:
        print("\033[41mNo lyrics found\033[000m\n")
    else:
        print("Error "+str(response.status_code))
        return
    
def get_songs(start_dir):
    music_files = []

    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if str(file).lower().endswith(('.mp3', '.flac')) and not str(file).lower().startswith('._'):
                music_files.append(str(root+'/'+file))

    return music_files

def get_metadata(song):
    metadata = mutagen.File(song)
    return metadata

def replace_characters(string):
    updated_string = string.replace('/', '_').replace('<', '').replace('>', '').replace(':', '').replace('"', '').replace('|', '').replace('?', '').replace('*', '')
    return updated_string

# "TALB": "album"
# "TIT2": "title"
# "TPE2": "albumartist"
# "TRCK": "tracknumber"
# "USLT": "unsynchronizedlyrics"
# "SYLT": "synchronizedlyrics"
# \033[XXXm

not_found = []
found = []

if len(sys.argv) == 1:
    print("Please enter a file location")
    sys.exit()

songs = get_songs(str(sys.argv[1]))

print("\nSongs found: "+str(len(songs))+"\n")

songs.sort()

iteration = 0
for song in songs:
    iteration += 1

    # Check if lyrics exist
    if os.path.isfile(str(song).replace('.flac', '').replace('.mp3', '')+".lrc"):
        print("Lyrics already exist. skipping...\n")
        continue

    # Get metadata
    try: meta = get_metadata(song)
    except:
        print("\033[41mNo metadata found for "+str(song)+" \033[000m\n")
        continue
    
    if str(song).lower().endswith('.flac'):
        try: track = meta['title'][0]
        except:
            print("\033[41mNo title metadata found for "+str(song)+" \033[000m\n")
            continue
        try:
            if 'album artist' in meta:
                artist = meta['album artist'][0]
            else:
                artist = meta['albumartist'][0]
        except:
            print("\033[41mNo artist metadata found for "+str(song)+" \033[000m\n")
            continue
        try: album = meta['album'][0]
        except:
            print("\033[41mNo album metadata found for "+str(song)+" \033[000m\n")
            continue
        duration = round(meta.info.length)
    if str(song).lower().endswith('.mp3'):
        try: track = meta['TIT2'][0]
        except:
            print("\033[41mNo title metadata found for "+str(song)+" \033[000m\n")
            continue
        try: artist = meta['TPE2'][0]
        except:
            print("\033[41mNo artist metadata found for "+str(song)+" \033[000m\n")
        try: album = meta['TALB'][0]
        except:
            print("\033[41mNo album metadata found for "+str(song)+" \033[000m\n")
            continue
        duration = round(meta.info.length)

    print("\033[032m-----------------")
    print("\033[032mSong "+str(iteration)+" out of "+str(len(songs)))
    print("\033[032mTitle: "+track)
    print("\033[032mAlbum Artist: "+artist)
    print("\033[032mAlbum: "+album)
    print("\033[032mDuration (s): "+str(duration))
    print("\033[032m-----------------\033[000m\n")

    # Search for lyrics
    print("Searching lyrics for " + track + " by " + artist + "...\n")
    lyrics = get_lyrics(artist, track, album, duration)
    if lyrics:

        # Create lyrics file
        track_legal = str(song).replace('.flac', '').replace('.mp3', '')+".lrc"

        file = open(track_legal, 'w')
        print("Creating file " + track_legal +"...")
        file.write(lyrics)
        file.close()
        print("\033[102;030mDone\033[000m\n")
        found.append(song)

    else:
        not_found.append([track, artist])

print("Completed\n")
print("Lyrics found: "+str(len(found))+"\n")

if len(not_found) == 0:
    print("Lyrics not found: 0\n")
else:
    print("Lyrics not found: "+str(len(not_found))+", Listing:\n")

    for song in not_found:
        print('\033[31m'+song[1]+' - '+song[0]+'\033[0m')
    print('')
