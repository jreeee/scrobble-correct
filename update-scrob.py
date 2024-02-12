#! /bin/env/python3

import pathlib
import json
import sys
import os
import unicodedata

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
        padding_max = 80
        string = ""
        if self.Album_Artist == None:
            if self.Album == None:
                string = f"< {self.Url} > | {self.Title} - {self.Artist}"
            else:
                string = f"< {self.Url} > | {self.Title} - {self.Artist}, {self.Album}"
        else:
            string = f"< {self.Url} > | {self.Title} - {self.Artist}, {self.Album} - {self.Album_Artist}"

        strlen = getlen(string)
        if strlen < padding_max:
            string = string + " "*(padding_max - strlen) + self.Link
        else:
            #string = string[0:padding_max-4] + "... " + self.Link
            print("lol")
        return string

def getlen(string):
    i = 0
    hw = 0
    for char in string:
        char_type = unicodedata.east_asian_width(char)
        if char_type == 'W':
            i = i + 2
        elif char_type == 'H':
            if hw == 1:
                hw = 0
            else:
                hw = 1
                i = i + 1
        else:
            i = i + 1
    return i

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
    for i in l1.len:
        for j in l2.len:
            if i == j:
                combine(i, j, mode)

def combine(el1, el2, mode):
    if mode == 'i':
        return el2
    elif mode == 'e':
        return el1
    else:
        manual_combine(el1, el2)

def manual_combine(el1, el2):
    # input check
    if input == 'e' or input == 'i':
        combine(el1, el2, input)
    elif input == 'm':
        # create a object field by field using manual_select and return it
        print("todo")
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
    for i in list:
        print(i)
#def move(list, dir):


def main():
    BASE_PATH = pathlib.Path(__file__).parent.resolve()
    COMBINED_FILE = os.path.join(BASE_PATH, "combined.json")
    print(COMBINED_FILE)
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

    print_list(list_cm)

    print_list(list_im)

    #compare (combined, imported, COMBINEMODE)

    #move(FINISH_PATH, MOVE_MODE)


if __name__ == "__main__":
    main()
