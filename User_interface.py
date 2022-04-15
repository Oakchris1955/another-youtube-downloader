#import tkinter module
import tkinter as tk
import tkinter.ttk as ttk

#import threading module
from threading import *

#import the functions module
from functions import *

class MainUI:
	def __init__(self, root):
		self.root = root

		#make a table to show the links
		self.tree = ttk.Treeview(self.root, columns=('Number', 'Name', 'URL', 'Status'), height=5, show='headings')

		#modify the table columns
		self.tree.heading('Number', text='#')
		self.tree.column('Number', width=30)
		self.tree.heading('Name', text='Video Name')
		self.tree.column('Name', width=270)
		self.tree.heading('URL', text='Video URL')
		self.tree.column('URL', width=270)
		self.tree.heading('Status', text='Video status')
		self.tree.column('Status', width=270)

		#bind function for when something is selected
		self.tree.bind('<<TreeviewSelect>>', lambda event:functions.on_tree_selection(event))

		#grid the table
		self.tree.grid(row=0, column=0)


		#video options frame
		self.options_frame = tk.Frame(self.root)
		self.options_frame.grid(row=0, column=1)

		#audio format selector
		self.audio_formats = ttk.Combobox(self.options_frame, state='readonly', values=['None'])
		self.audio_formats.set('None')
		self.audio_formats.bind('<<ComboboxSelected>>', lambda event:functions.on_audioformat_selection(event))
		self.audio_formats.grid(row=0, column=0, columnspan=2, pady=10, padx=5)

		#audio format properties
		self.audio_size = tk.Label(self.options_frame, text='Audio info unavailable')
		self.audio_size.grid(row=1, column=0)

		#audio format extension
		self.audio_extension = tk.Label(self.options_frame, text='Audio info unavailable')
		self.audio_extension.grid(row=1, column=1)


		#video format selector
		self.video_formats = ttk.Combobox(self.options_frame, state='readonly',values=['None'])
		self.video_formats.set('None')
		self.video_formats.bind('<<ComboboxSelected>>', lambda event:functions.on_videoformat_selection(event))
		self.video_formats.grid(row=2, column=0, columnspan=2, pady=10, padx=5)

		#video format properties
		self.video_size = tk.Label(self.options_frame, text='Video info unavailable')
		self.video_size.grid(row=3, column=0)

		#video format extension
		self.video_extension = tk.Label(self.options_frame, text='Video info unavailable')
		self.video_extension.grid(row=3, column=1)


		#download button
		self.download_button = tk.Button(self.options_frame, text='Start downloading', command=lambda:threading.Thread(target=functions.on_downloadbutton_click).start())
		self.download_button.grid(row=4, column=0, columnspan=2)

		#make a frame for the download input
		self.input_frame = tk.Frame(self.root)
		self.input_frame.grid(row=1, column=0, columnspan=2)

		#input entry bar
		self.link_entry = tk.Entry(self.input_frame, width=140)
		self.add_button = tk.Button(self.input_frame, text='+', width=3, command=lambda:threading.Thread(target=functions.insert_video, args=[self.link_entry.get()]).start())
		self.remove_button = tk.Button(self.input_frame, text='-', width=3, command=lambda:functions.remove_video())


		#error viewer
		self.error_viewer = tk.Text(self.root, state=tk.DISABLED, height=5, width=130, font=('Arial','10'))


		#grid the widgets
		self.link_entry.grid(row=0, column=0, padx=5)
		self.add_button.grid(row=0, column=1, padx=2)
		self.remove_button.grid(row=0, column=2, padx=2)

		#grid the error viewer
		self.error_viewer.grid(row=2, column=0, columnspan=2)


		#disable window resizing
		self.root.resizable(False, False)


		#initialize the function class
		functions = functions_class(self)