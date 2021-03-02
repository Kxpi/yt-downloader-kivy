from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.lang import Builder 
from kivy.config import Config
from kivy.core.window import Window 
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from os import path
from time import sleep
import pytube


Config.set('input', 'mouse', 'mouse,multitouch_on_demand') #turns off multitouch to prevent from orange dots on screen

#defining screens 

class Choice_screen(Screen):
	pass

class Single_file_screen(Screen):

	#this function makes it impossible to save a file other than in directory
	def selected(self, filename):
		global s_directory  #stands for single file directory

		try:
			s_directory = filename[0]

			if path.isdir(s_directory):
				pass
			else:
				for i in range(len(s_directory), -1, -1):
					if s_directory[i]==r"/":
						s_directory.pop(i)
					else:
						s_directory.pop(i)
						break

			self.ids.selected_directory.text=f'File will be saved in: {s_directory}'

		except:
			pass

	def choosen_link(self):
		global hyperlink_single #link for single file download
		hyperlink_single=self.ids.video_link.text

	def vid_or_not_vid(self, decision):
		global with_video_s
		with_video_s=decision

	

class Playlist_screen(Screen):

	#this function makes it impossible to save files other than in directory
	def selected(self, filename):
		global p_directory #stands for playlist directory

		try:
			p_directory = filename[0]

			if path.isdir(p_directory):
				pass
			else:
				for i in range(len(p_directory), -1, -1):
					if p_directory[i]==r"/":
						p_directory.pop(i)
					else:
						p_directory.pop(i)
						break

			self.ids.selected_directory.text=f'File will be saved in: {p_directory}'
			

		except:
			pass

	def choosen_link(self):
		global hyperlink_playlist #link for download of a whole playlist
		hyperlink_playlist=self.ids.playlist_link.text

	def vid_or_not_vid(self, decision):
		global with_video_p
		with_video_p=decision
	



class Outcome_screen_single(Screen):

	#single audio download
	def s_a(self, *args): 
		try:
			link=(hyperlink_single).strip()

			pytube.YouTube(link).streams.filter(only_audio=True).first().download(s_directory)

			self.ids.output.text='Download successful'
		except:
			self.ids.output.text="It's not a valid link / video is set to private"

	#single video download
	def s_v(self, *args):
		try:
			link=(hyperlink_single).strip()

			pytube.YouTube(link).streams.get_highest_resolution().download(s_directory)

			self.ids.output.text='Download successful'
		except:
			self.ids.output.text="It's not a valid link / video is set to private"


	#these were neccessary to properly time changing screen and starting one of these functions (1 stands for 1 second delay)

	def download_single(self, *args): 
		if with_video_s==True:
			Clock.schedule_once(self.s_v, 1)
		else:
			Clock.schedule_once(self.s_a, 1)

	def clear_output(self):
		self.ids.output.text='...'


class Outcome_screen_playlist(Screen):

	#playlist audio download
	def p_a(self, *args):
		i=0
		log=''

		try:
			#getting a playlist link and creating Playlist object

			playlist_link=(hyperlink_playlist).strip()

			playlist=pytube.Playlist(playlist_link)

			#check if list with urls was obtained correctly
			if len(playlist)>0:

				for url in playlist:
					i+=1
					try:
						#for each url in list an attempt for downloading is taken 
		   				pytube.YouTube(url).streams.filter(only_audio=True).first().download(p_directory)
		   				#if it succeeds, user is informed about this fact,
		   				log+=f'{i}. {url} - Successful \n'

					except:	
						#if download fails, user is notified and knows exact file that wasn't downloaded
						log+=f'{i}. {url} - Error \n'

					self.ids.output.text=log

			else:
				self.ids.output.text="It's not a valid playlist link / it's set to private"
		except:
			self.ids.output.text="It's not a valid playlist link / it's set to private"


	#playlist video download
	def p_v(self, *args):
		i=0
		log=''

		try:
			#getting a playlist link and creating Playlist object

			playlist_link=(hyperlink_playlist).strip()
			
			playlist=pytube.Playlist(playlist_link)
			
			#check if list with urls was obtained correctly
			if len(playlist)>0:

				for url in playlist:
					i+=1
					try:

						#for each url in list an attempt for downloading is taken 
		   				pytube.YouTube(url).streams.get_highest_resolution().download(p_directory)

		   				#if it succeeds, user is informed about this fact,
		   				log += f'{i}. {url} - Successful \n'

					except:	

						#if download fails, user is notified and knows exact file that wasn't downloaded
						log += f'{i}. {url} - Error \n'

					self.ids.output.text=log

			else:
				self.ids.output.text="It's not a valid playlist link / it's set to private"
		except:
			self.ids.output.text="It's not a valid playlist link / it's set to private"


	#these were neccessary to properly time changing screen and starting one of these functions (1 stands for 1 second delay)

	def download_playlist(self, *args):
		if with_video_p==True:
			Clock.schedule_once(self.p_v, 1)
		else:
			Clock.schedule_once(self.p_a, 1)

	def clear_output(self):
		self.ids.output.text=''
		

class WindowManager(ScreenManager):
	pass



class DownloaderApp(App):
	icon='images/yt_logo.png'
	
	def build(self):
		Window.clearcolor=(52/255, 54/255, 54/255, 1)
		self.Outcome_screen_playlist = Outcome_screen_playlist()
		self.Outcome_screen_single = Outcome_screen_single()


if __name__ == '__main__':
	DownloaderApp().run()