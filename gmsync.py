#!/usr/bin/env python3
# coding=utf-8

"""
An upload script for Google Music using https://github.com/simon-weber/gmusicapi.

Usage:
  Run gmsync from the directory that contains mp3 files.
 
Arguments:
  None	  

Options:
  None

"""

import logging
import os
import sys

from gmusicapi_wrapper import MusicManagerWrapper


logger = logging.getLogger('gmusicapi_wrapper')
sh = logging.StreamHandler()
logger.addHandler(sh)


def main():
	logger.setLevel(logging.INFO)

	mmw = MusicManagerWrapper(True)
	mmw.login()

	if not mmw.is_authenticated:
		sys.exit()

	songs_to_upload, songs_to_filter, songs_to_exclude = mmw.get_local_songs(os.getcwd(), None, None, False, False, "", float('inf'))

	songs_to_upload.sort()
	songs_to_exclude.sort()


	if songs_to_upload:
		logger.info("\nUploading {0} song(s) to Google Music\n".format(len(songs_to_upload)))

		mmw.upload(songs_to_upload, "", False)
	else:
		logger.info("\nNo songs to upload")

	logger.info("Remove duplicates...")
	all_songs = mmw.get_google_songs()
	new_songs = {}
	old_songs = {}
	for song in all_songs[0]:
		song_id = song['id']		
		if song['disc_number'] is None:
			discnum = 0
		else:
			discnum = song['disc_number']
	
		if song['track_number'] is None:
			tracknum = 0
		else: 
			tracknum = song['track_number']
	
		key = "%s: %d-%02d %s" % ( song['album'], discnum, tracknum, song['title'] )
	
		if key in new_songs:
			old_songs[key] = { 'id': song_id }
	
		new_songs[key] = { 'id': song_id}

	if len( old_songs ):
		print('Duplicate songs')
	
		old_song_ids = []
	
		for key in sorted( old_songs.keys() ):
			old_song_ids.append( old_songs[key]['id'] )
			print('	   ' + str(key.encode('utf-8')))
	
		print('Deleting songs ...')
		mmw.delete_songs( old_song_ids )
	else:
		print('No duplicate songs.')

	mmw.logout()
	logger.info("\nAll done!")

if __name__ == '__main__':
	main()
