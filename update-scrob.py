#! /usr/bin/env python3

import pathlib
import json
import shutil
import time
import os
import unicodedata

class SongURL:
    artist = ""
    track = ""
    album = ""
    albumArtist = ""
    def __init__(self, a, t, b, r):
        self.artist = a
        self.track = t
        self.album = b
        self.albumArtist = r

class SongJSON:
    Song_Url = None
    def __init__(self, a, t, b, r):
        self.Song_Url = SongURL(a, t, b, r)

    def toJSON(self, url):
        return json.dumps({url : self.Song_Url}, default=lambda o: o.__dict__, sort_keys=False, ensure_ascii=False)

class Song:
    Url = "url"
    Link = None
    Title = "title"
    Artist = "artist"
    Album = None
    Album_Artist = None
    def __init__(self, url, title, artist, album=None, album_artist=None):
        self.Url = url
        self.Link = f"https://youtu.be/{url}"
        self.Title = title
        self.Artist = artist
        self.Album = album
        self.Album_Artist = album_artist

    def __str__(self):
        padding_max = 60
        string = ""
        if self.Album_Artist == None:
            if self.Album == None:
                string = f"{self.Url} | {self.Title} - {self.Artist}"
            else:
                string = f"{self.Url} | {self.Title} - {self.Artist}, {self.Album}"
        else:
            string = f" {self.Url} | {self.Title} - {self.Artist}, {self.Album} - {self.Album_Artist}"

        string = setlen(string, padding_max) +  "| " + self.Link
        return string

    def toJSON(self):
        return SongJSON(self.Artist, self.Title, self.Album, self.Album_Artist).toJSON(self.Url)

def setlen(string, padding_max):
    #todo refactor
    i = 0
    for j in range(len(string)):
        step = 0
        char_type = unicodedata.east_asian_width(string[j])
        if char_type == 'W' or char_type == 'F':
            i = i + 2
            step = 1
        #elif char_type == 'H':
        #    if hw == 1:
        #        hw = 0
        #    else:
        #        hw = 1
        #        i = i + 1
        else:
            i = i + 1

        #edgecases because we cant have nice things
        if i >= padding_max:
            if padding_max == i and step == 1:
                return string[0:j] + ">"
            elif padding_max < i and step == 1:
                ct = unicodedata.east_asian_width(string[j-1])
                if ct == 'W' or ct == 'F':
                    return string[0:j-1] + " >"
                else:
                    return string[0:j-1] + ">"
            else:
                return string[0:j-1] + ">"

    return string + " "*(padding_max-i-1)

def load_list(file_path):
    if not check_path(file_path, False):
        print(f"no such file {file_path}")
        return
    songs = []
    with open(file_path, "r+", encoding="utf-8") as f:
        entries = json.loads(f.read())
        for i in entries:
            s = Song(i, entries[i]["track"], entries[i]["artist"], entries[i]["album"], entries[i]["albumArtist"])
            songs.append(s)

    return songs


def check_path(path, is_dir):
    if is_dir:
        return os.path.isdir(path)
    return os.path.exists(path)

def compare(l1, l2, mode):
    tmp = []
    for i in l1:
        unique = True
        for j in l2:
            if i.Url == j.Url:
                unique = False
                combine(i, j, mode)
                break
        if unique:
            tmp.append(i)

    return l1 + tmp

def combine(el1, el2, mode):
    if mode == 'i':
        el1 = el2
    elif mode == 'e':
        return
    else:
        manual_combine(el1, el2)

def manual_combine(el1, el2):
    # input check
    if input == 'e' or input == 'i':
        combine(el1, el2, input)
    elif input == 'c':
        # create a object field by field using manual_select and return it
        title = input("Song Title")
        artist = input("Artist")
        album = input("Album")
        albumartist = input("Album Artist")
        el1 = Song(title, artist, album, albumartist)
    elif input == 'm':
        el1.Title = manual_select(el1.Title, el2.Title)
        el1.Artist = manual_select(el1.Artist, el2.Artist)
        el1.Album = manual_select(el1.Album, el2.Album)
        el1.AlbumArtist = manual_select(el1.AlbumArtist, el2.AlbumArtist)
    else:
        print("wrong input")
        manual_combine(el1, el2)

def manual_select(at1, at2):
    # input check
    if input == 'i':
        return at1
    elif input == 'e':
        return at2
    elif input == 'm':
        # get input
        return input("enter text")
    else:
        print("wrong input")
        manual_select(at1, at2)

def print_list(list):
    for i in range(len(list)):
        print(str(list[i]) + " " + str(i))

def move(fpd, fpi, mode, list_cm, fpb, fpc):
    #if mode == 'b':
    fp = os.path.join(fpb, "export.json")
    with open(fp, "w+", encoding="utf-8") as f:
        f.write("{\n")
        first = True
        for i in list_cm:
            if first:
                comma = ""
                first = False
            else:
                comma = ",\n"
            f.write(comma + (i.toJSON()[1:-1]))
        f.write("\n}")

    timestr = time.strftime("%Y%m%d-%H%M%S")
    shutil.move(fpi, os.path.join(fpd, "cache-" + timestr + ".json"))
    shutil.move(fpc, os.path.join(fpd, "combined-" + timestr + ".json"))
    shutil.move(fp , fpc)

def main():
    BASE_PATH = pathlib.Path(__file__).parent.resolve()
    COMBINED_FILE = os.path.join(BASE_PATH, "combined.json")
    # can be overridden, link to json/dir with jsons
    # [-p /link/to/file], cant use the combined file?
    IMPORT_FILE = os.path.join(BASE_PATH, "import/local-cache.json")
    # stores the used json files for backup
    FINISH_PATH = os.path.join(BASE_PATH, "imported")
    #options: move file to backup, do nothing with the file, delete, replace with combined
    # [-m [b], n, d, r] otherwise interpret as fp
    MOVE_MODE = 'b'
    COMBINE_MODE = 'e'
    #input handeling

    list_cm = load_list(COMBINED_FILE)

    list_im = load_list(IMPORT_FILE)

    #combine lists
    list_res = compare(list_im, list_cm, COMBINE_MODE)

    #eliminate double elements
    list_fin = compare(list_res, list_res, COMBINE_MODE) 

    print_list(list_fin)

    move(FINISH_PATH, IMPORT_FILE, MOVE_MODE, list_fin, BASE_PATH, COMBINED_FILE)


if __name__ == "__main__":
    main()
