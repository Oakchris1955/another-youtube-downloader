#the message handler
class Logger:
	def __init__(self, UI):
		self.UI = UI

	def debug(self, msg):
		# For compatibility with youtube-dl, both debug and info are passed into debug
		# You can distinguish them by the prefix '[debug] '
		if msg.startswith('[debug] '):
			print(msg)
		else:
			self.info(msg)

	def info(self, msg):
		if msg.startswith('[download] '):
			self.download(msg)
		print(msg)

	def warning(self, msg):
		print(msg)

	def error(self, msg):
		print(msg)
	
	def download(self, msg):
		#if msg.endswith('downloaded'):
		#	self.UI.progress_label.config(text='Video already downloaded')
		print(msg)