import sublime, sublime_plugin, os,time, commands
from datetime import datetime, timedelta

class FaceCodeCommand(sublime_plugin.EventListener):

	def __init__(self):
		self.cnt         = 1
		self.settings    = sublime.load_settings("FaceCode.sublime-settings")
		self.facecode    = self.settings.get("facecode")
		self.time_format = self.settings.get("time_format")
		self.img_format  = self.settings.get("img_format")
		self.path_photo  = self.settings.get("path_save_photo")
		self.path_screen = self.settings.get("path_save_screen")
		self.device      = self.settings.get("device")
		self.count_save  = self.settings.get("count_save")
		self.filename 	 = self.get_file_name()
		self.check_folder()
	
	def on_pre_save(self, view):
		if self.facecode:
			if self.cnt % self.count_save == 0:
				self.save_photo()
				self.save_screen()
			self.cnt += 1

	def check_folder(self):
		if not os.path.exists(self.path_photo) and self.path_photo:
			os.mkdir(self.path_photo, 0777)
		if not os.path.exists(self.path_screen) and self.path_screen:
			os.mkdir(self.path_screen, 0777)
		return

	def get_file_name(self):
		date_time = datetime.now()
		date_time = str(date_time.strftime(self.time_format))
		return date_time+"."+self.img_format

	def save_photo(self):
		os.system("streamer -c "+self.device+" -o "+self.path_photo+self.filename)
		return

	def save_screen(self):
		win_id = commands.getoutput('xprop -root | grep "_NET_ACTIVE_WINDOW(WINDOW)" | awk \'{print $5}\'')
		os.system("import -window "+win_id+" "+self.path_screen+self.filename)
		return