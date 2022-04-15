#import the Youtube video downloader
import yt_dlp

#import the logger
from logger import Logger

#import the time module to get UNIX timestamp
from time import time

#import datetime to get readable version of current time
from datetime import datetime

#import the tkinter module
import tkinter as tk
import tkinter.ttk as ttk

#import os module to get download folder
import os

#import threading module
import threading

#import json to serialise dicts to strings
import json


#create some custom exceptions
class DownloadAborted(Exception):
	#raisen when download was interrupted by user
	pass

#main fucntions class
class functions_class:
	def __init__(self, UI):
		self.UI = UI
		self.previous_selection = []



	def insert_to_err_logger(self, text):
		self.UI.error_viewer.configure(state=tk.NORMAL)
		self.UI.error_viewer.insert(tk.END, datetime.now().strftime('At %H:%M:%S : ')+text+'\n')
		self.UI.error_viewer.configure(state=tk.DISABLED)


	def get_video_info(self, video_link):
		self.UI.root.update_idletasks()
		with yt_dlp.YoutubeDL({'simulate':True}) as ydl:
			self.UI.root.update_idletasks()
			json_info = ydl.sanitize_info(ydl.extract_info(video_link))
			return json_info

	def extract_formats(self, input_info):
		#extract formats from video info dict
		output_info = {'audio_formats':[], 'video_formats':[]}

		for i in input_info['formats']:
			if i['audio_ext'] != 'none':
				if i['filesize'] is None:
					i['filesize'] = i['filesize_approx']
				output_info['audio_formats'].append({'extension': i['audio_ext'], 'filesize':i['filesize'], 'id':i['format_id']})

			if i['video_ext'] != 'none':
				if i['filesize'] is None:
					i['filesize'] = i['filesize_approx']
				output_info['video_formats'].append({'extension': i['video_ext'], 'filesize':i['filesize'], 'id':i['format_id']})
		return output_info



	def abort_video_on_deletion_progress_hook(self, response):
		#check if the video currently downloading was deleted
		for iid in self.UI.tree.get_children():
			print(self.UI.tree.set(iid, 'Name'))
			if response['info_dict']['title'] == self.UI.tree.set(iid, 'Name'):
				return

		#if nothing is found, raise an exception
		raise DownloadAborted


	def update_progressbar(self, response):
		#find which item the name corresponds to
		for iid in self.UI.tree.get_children():
			print(self.UI.tree.set(iid, 'Name'))
			if response['info_dict']['title'] == self.UI.tree.set(iid, 'Name'):
				saved_iid = iid

		#check if the video is downloading
		if response['status'] == 'downloading':

			#calculate the percentage
			fragment_downloaded = round(float(response['downloaded_bytes'])/float(response['total_bytes'])*100, 1)

			#check if what is currently downloading is video or audio
			if response['info_dict']['audio_ext'] == 'none':
				filetype = 'video'
			elif response['info_dict']['video_ext'] == 'none':
				filetype = 'audio'

			#update the status bar
			self.UI.tree.set(iid, 'Status', f'{fragment_downloaded}% downloaded (of {filetype})')

		elif response['status'] == 'finished':
			#check if what is currently downloading is video or audio
			if response['info_dict']['audio_ext'] == 'none':
				filetype = 'Video'
			elif response['info_dict']['video_ext'] == 'none':
				filetype = 'Audio'


			#if video/audio finished downloading, update status bar
			self.UI.tree.set(iid, 'Status', f'{filetype} downloaded')





	def on_tree_selection(self, event):
		#get selected items
		tree = event.widget
		#get iids of selected items
		selection_ids = [item for item in tree.selection()]

		if not selection_ids:
			#if nothing is selected, empty the format selection boxes
			self.UI.audio_formats['values'] = ('None')
			self.UI.audio_formats.set('None')

			self.UI.video_formats['values'] = ('None')
			self.UI.video_formats.set('None')

		elif json.loads(self.UI.tree.item(selection_ids[0])['tags'][0])['status'] == 'Not ready':
			return
		elif self.previous_selection == selection_ids:
			return
		else:
			#else, fill it with the available formats

			#get the available formats
			all_formats = json.loads(self.UI.tree.item(selection_ids[0])['tags'][0])

			#split the available formats to video and audio
			audio_formats = all_formats['audio_formats']
			video_formats = all_formats['video_formats']

			#insert the formats to selection box
			self.UI.audio_formats['values'] = ['bestaudio']+[audio['id'] for audio in audio_formats]
			self.UI.audio_formats.set('bestaudio')

			self.UI.audio_size.config(text='Audio info unavailable')
			self.UI.audio_extension.config(text='Audio info unavailable')

			self.UI.video_formats['values'] = ['bestvideo']+[video['id'] for video in video_formats]
			self.UI.video_formats.set('bestvideo')

			self.UI.video_size.config(text='Video info unavailable')
			self.UI.video_extension.config(text='Video info unavailable')

			self.previous_selection = selection_ids


	def on_audioformat_selection(self, event):
		#set the selection format to be that selected
		self.UI.audio_formats.set(self.UI.audio_formats.get())

		#get iids of selected items
		selection_ids = [item for item in self.UI.tree.selection()]

		#change the audio size and extension to the equivalant for that format id
		all_formats = json.loads(self.UI.tree.item(selection_ids[0])['tags'][0])

		#check if selection is "bestaudio"
		if self.UI.audio_formats.get() == "bestaudio":
				self.UI.audio_size.config(text="Audio info unavailable")
				self.UI.audio_extension.config(text="Audio info unavailable")
		else:
			#else, get corresponding info for format
				for audio_format in all_formats['audio_formats']:
					if audio_format['id'] == self.UI.audio_formats.get():
						self.UI.audio_size.config(text=f"Filesize of audio:\n{audio_format['filesize']} bytes")
						self.UI.audio_extension.config(text=f"Audio extension:\n.{audio_format['extension']}")
						break


		print(self.UI.audio_formats.get())


	def on_videoformat_selection(self, event):
		#set the selection format to be that selected
		self.UI.video_formats.set(self.UI.video_formats.get())

		#get iids of selected items
		selection_ids = [item for item in self.UI.tree.selection()]

		#change the video size and extension to the equivalant for that format id
		all_formats = json.loads(self.UI.tree.item(selection_ids[0])['tags'][0])

		#check if selection is "bestvideo"
		if self.UI.video_formats.get() == "bestvideo":
				self.UI.video_size.config(text="Video info unavailable")
				self.UI.video_extension.config(text="Video info unavailable")
		else:
			#else, get corresponding info for format
			for video_format in all_formats['video_formats']:
				if video_format['id'] == self.UI.video_formats.get():
					self.UI.video_size.config(text=f"Filesize of video:\n{video_format['filesize']} bytes")
					self.UI.video_extension.config(text=f"Video extension:\n.{video_format['extension']}")
					break


		print(self.UI.video_formats.get())


	def on_downloadbutton_click(self):
		#check if a queued video is selected
		if not self.UI.tree.selection():
			return

		#if yes, check if the selected video doesn't have the available info yet

		#get iids of selected items
		selection_ids = [item for item in self.UI.tree.selection()]

		#get the json info
		all_formats = json.loads(self.UI.tree.item(selection_ids[0])['tags'][0])

		#check if the vid is ready
		if all_formats['status'] == 'Not ready':
			return

		#start downloading the video with selected formats
		ydl_opts = {
			#save the video to downloads folder
			'outtmpl': str(os.path.join(os.getenv('USERPROFILE'), 'Downloads'))+'/'+'%(title)s.%(ext)s',
			#unused logger
			'logger': Logger(self.UI),
			#pass the selected formats
			'format':f'{self.UI.video_formats.get()}+{self.UI.audio_formats.get()}',
			#define the progress hooks: one to abort downloading when video is removed from queue and another to update the progress bar
			'progress_hooks':[self.abort_video_on_deletion_progress_hook, self.update_progressbar]
		}

		#get the video URL
		url = self.UI.tree.set(selection_ids[0], 'URL')

		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			#also handle any errors
			try:
				ydl.download([url])
			except yt_dlp.DownloadError:
				self.insert_to_err_logger('Please check your internet connection')
			#if download was aborted by user, send a debug message
			except DownloadAborted:
				self.insert_to_err_logger(f'The video with URL: {url} was removed from queue. Aborting download')



	def insert_video(self, video_link):
		'''Add the video to the queue'''
		#update the UI
		self.UI.root.update_idletasks()
		#get the current time as a UNIX timestamp
		iid = time()
		#insert a row in the table
		self.UI.tree.insert("", "end", values=(self.get_highest_column_id(0)+1, 'Processing...', str(video_link), 'Processing...'), iid=iid, tags=f"{{{json.dumps({'status':'Not ready'})}}}")
		self.UI.root.update_idletasks()
		#update the name of the video in the row
		try:
			#get video info
			json_info = self.get_video_info(video_link)
		except yt_dlp.DownloadError as error_msg:
			#if error occurs, output it to error logger
			self.UI.tree.delete(iid)
			self.insert_to_err_logger(str(error_msg))
		else:
			#else, check if the link inputed is already queued for downloading
			URL_list = []
			for value in self.get_all_values().values():
				URL_list.append(value[2])
				print(value[2])
			URL_list.remove(video_link)

			#if inputed, remove the item from download queue
			if (json_info['webpage_url'] in URL_list):
				self.UI.tree.delete(iid)
				
				#also, change the column ids so that they escalate
				for i, item in enumerate(self.UI.tree.get_children()):
					self.UI.tree.set(item, column=0, value=i+1)
			else:
				#if not inputed already, change the "Processing..." status
				self.UI.tree.set(iid, 'Name', json_info['title'])
				self.UI.tree.set(iid, 'Status', 'Ready to be downloaded')
				#also, change the text inputed to an actual URL
				self.UI.tree.set(iid, 'URL', json_info['webpage_url'])
				#and save the video formats in a json format as tag
				formats = self.extract_formats(json_info)
				self.UI.tree.item(iid,
								tags=('{'+
									json.dumps(
										{
											'status': 'Ready',
											'audio_formats': formats['audio_formats'],
											'video_formats': formats['video_formats']
										}
									)
								+'}')
						)
				#re-select the videos to trigger a selection event and update the comboboxes
				self.UI.tree.selection_set(self.UI.tree.selection())

				#for those wondering why I put those extra brackets, for some reason the tag is parsed without them if I don't add them

	def remove_video(self):
		'''Remove the video from the queue'''
		if self.UI.tree.selection() != ():
			for item in self.UI.tree.selection():
				self.UI.tree.delete(item)

			#change the column ids so that they escalate
			for i, item in enumerate(self.UI.tree.get_children()):
				self.UI.tree.set(item, column=0, value=i+1)

			#also, change the format values to None
			self.UI.audio_formats['values'] = ['None']
			self.UI.audio_formats.set('None')

			self.UI.audio_size.config(text='Filesize of audio:\nNot selected anything yet')
			self.UI.audio_extension.config(text='Audio extension:\nNot selected anything yet')


			self.UI.video_formats['values'] = ['None']
			self.UI.video_formats.set('None')

			self.UI.video_size.config(text='Filesize of video:\nNot selected anything yet')
			self.UI.video_extension.config(text='Video extension:\nNot selected anything yet')



	def get_all_values(self):
		'''Gets values of all items'''
		all_values = {}
		for child in self.UI.tree.get_children():
			all_values[child] = self.UI.tree.item(child)["values"]
		print(all_values)
		return all_values

	def get_highest_column_id(self, column_numb):
		'''Get the highest video id'''
		highest_value = 0
		for child in self.UI.tree.get_children():
			values = self.UI.tree.item(child)["values"]
			#check if value is highest than the highest stored value
			if values[column_numb] > highest_value:
				highest_value = values[column_numb]
		return highest_value