#! /bin/env/python3

import pathlib
import json
import sys

def load_list(file_path):
	if not check_path(file_path, False)
		print("no such file {file_path}")
		sys.exit(1)
	return json.loads(file_path)["data"]

def check_path(path, is_dir):
	if is_dir:
		return os.path.isdir(path)
	return os.path.exists(path)

def compare(l1, l2, mode):
	for i in l1.len:
		for j in l2.len:
			if i == j:
				combine(i, j, mode)

def combine(el1, el2, mode)
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
	else:
        print("wrong input")
		manual_combine(el1, el2)

def manual_select(at1, at2):
	# input check
	if input == 'i'
		return at1
	elif input == 'e':
		return at2
	elif input == 'm'
		# get input
		return input_str
	else:
		print("wrong input")
		manual_select(at1, at2)

def move(list, dir):


def main():
	BASE_PATH = pathlib.Path(__file__).parent.resolve()
	COMBINED_FILE = os.path.join(BASE_PATH, "/combined.json")
	# can be overridden, link to json/dir with jsons
	# [-p /link/to/file], cant use the combined file?
	IMPORT_FILE = os.path.join(BASE_PATH, "/import/local-cache.json")
	# stores the used json files for backup
	FINISH_PATH = os.path.join(BASE_PATH, "/imported")
	#options: move file to backup, do nothing with the file, delete, replace with combined
	# [-m [b], n, d, r] otherwise interpret as fp
	MOVE_MODE = 'b'
	COMBINE_MODE = 'e'
	#input handeling

	combined = load_list(COMBINED_FILE)
	imported = load_list(IMPORT_FILE)

	compare (combined, imported, COMBINE_MODE)

	move(FINISH_PATH, MOVE_MODE)


if __name__ == "__main__"
