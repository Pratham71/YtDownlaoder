import moviepy.editor
from pytube import YouTube
from youtubesearchpython import VideosSearch
from time import perf_counter
import os
import moviepy
from num2words import num2words

class YTDownloader:
    Nothing = str
    def __init__(self,link:str = None,path:str="Downloades")->Nothing:
        self.__cwd = os.getcwd()
        
        self.link = link
        self.path = path
    
        try:
            os.chdir(self.path)
        except FileNotFoundError:
            os.mkdir(self.path)
        finally:
            os.chdir(self.__cwd)
   
    def Download(self):
        if self.link is None:
            raise ValueError("No link was provided")

        yt=YouTube(self.link)
        data:dict[str,str|int]={
        "title":yt.title,
        "length":yt.length//60,
        "Views":num2words(yt.views),
        }
        print(f"Now Donloading: {data["title"].upper()}")
        start=perf_counter()
        print(f'TITLE:{data["title"]}\nLENGHT:{data["length"]} mins\nVIEWS:{data["Views"]}')
        yd=yt.streams.get_highest_resolution()
        yd.download(self.path)
        end=perf_counter()
        print(f"download took: {end-start}s")
        print("+====+====+====+====+====+====+====+====+====+====+====+====+====+====+====+====+\n")
    
    def to_mp3(self,mp4_path:bool = None):
        """downloads mp3 audio of all videos in 'downloads' dir."""
        if mp4_path is None:
            raise ValueError("No mp4 video path was given")
        else:
            title = YouTube(self.link).title
            video = moviepy.editor.VideoFileClip(mp4_path)
            mp3_title = title.lower().replace(" ","_") + ".mp3"
            mp3_title = mp3_title.replace("|","_")
            cwd = os.getcwd()
            os.chdir(self.path)
            os.system("mkdir mp3")
            os.chdir("mp3")
            video.audio.write_audiofile(mp3_title)
            os.chdir(cwd)
            print(f"Downloaded Mp3 file of '{title}'\n")
    
    def downloads(self)->list[str]|None:
        """Returns a list of total downloads in 'downloades' dir."""
        downloads =  [download for download in os.listdir(self.path)] or None
        if downloads is not None:
            downloads.pop(downloads.index("mp3"))
        return downloads

    def clear_folder(self,force:bool = False)->None:
        root_list:list[str] = [" ",".","/"]

        if self.path in root_list:
            raise FileNotFoundError("Directory doesnt exists.\nIf the program is placed in the same folder use 'clear_folder(force = True)' !!! NOTE THIS WILL REMOVE ALL MP3 OR MP4 FILES IN DIRECTORY !!!")
        elif force is True:
            self._clear()
        else:
            self._clear()
        print(f"Cleared folder: {self.path} and {self.path+"\\"+"mp3"}")
    
    def _clear(self)->None:
        for file in os.listdir(self.path):
            path = self.path + "\\" + file
            if path.endswith(".mp4"):
                os.remove(path)
            
        for file in os.listdir(self.path + "\\" + "mp3"):
            path = self.path + "\\" + "mp3" + "\\" + file
            if path.endswith(".mp3"):
                os.remove(path)

    def reveal_paths(self)->list[str]|None:
        """Returns a list[str] of all the downloads[path] in download folder, else returns None"""
        return [self.path+"\\"+path for path in os.listdir(self.path)]

    def get_links(self)->list[str]|None:
        """Returns a list[str] of all the downloads[links] in download folder, else returns None"""
        titles = [link.removesuffix(".mp4") for link in self.downloads()]

        links = []

        for title in titles:
            url = VideosSearch(title,limit=1).result()['result'][0]['link']
            links.append((title,url))
        
        return links
