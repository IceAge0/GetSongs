
import eyed3 
#import requests
from requests import get as requests_get
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
'''
https://music.163.com/#/song?id=1859245776
'''
songID=input().split('=')[-1]
getSong='https://music.163.com/song/media/outer/url?id='+songID+'.mp3'

print(type(songID))

class SongCatcher():
    def __init__(self,songID):
        self.songID=songID
        

    def get_title(self):
        getName='https://music.163.com/song?id='+songID
        songHTML=requests_get(getName, headers=headers)

        soup = BeautifulSoup(songHTML.text, 'lxml')
        #when <head> is to long to save as a file name in Windows,there'll be an error,so get from body

        song=(str(soup.body.find(class_="f-ff2")).split(">")[1]).split("<")[0]     #get song-singer,

        singer=(str(soup.body.find(class_="des s-fc4")).split(">")[-4]).split("<")[0]
        #bugs!!!when have more than one singer多个歌手显示最后一个的问题
        title=song +" - "+singer
        album_cover=soup.body.find(class_="u-cover u-cover-6 f-fl")     #type为bs4.element.Tag
        cover_url=str(album_cover).split("\"")[5]

        return title,cover_url



    def create_mp3(self,title):
        file_name=title+".mp3"
        getSong='https://music.163.com/song/media/outer/url?id='+songID+'.mp3'
        audio_content=requests_get(getSong, headers=headers).content
        print("正在写入"+file_name)
        with open(file_name,'wb') as f:     #create/rewrite
            f.write(audio_content)


    def change_cover(self,title,cover_url):
        
        file_name=title+".mp3"
        file_image=title+".jpg"
        urlretrieve(cover_url,file_image)       #download album cover
        print("changing album cover")
        audiofile = eyed3.load(file_name)
        if (audiofile.tag == None): 
            audiofile.initTag()
        audiofile.initTag()#bugs!!!!!
        audiofile.tag.images.set(3, open(file_image,'rb').read(), 'image/jpeg') 
        audiofile.tag.save(version=eyed3.id3.ID3_V2_3)

        cover_keep=input("Save album cover?(y/N)")
        if cover_keep == "y":
            pass
        else:
            import os
            os.remove(file_image)
#change 调用create，create调用get再return，以避免调用两次get的套圈写法?
catcher=SongCatcher(songID)
title,cover_url=catcher.get_title()
catcher.create_mp3(title)
catcher.change_cover(title,cover_url)

def get_lyrics(lyric_id,title):
    lyric_url='http://music.163.com/api/song/lyric?' + 'id=' + lyric_id + '&lv=1&kv=1&tv=-1'
    lyrics_txt=requests_get(lyric_url, headers=headers)
    file_name=title+".lrc"
    with open(file_name,'wb') as f:
    	f.write(lyrics_txt.content)

lyric_needs=input("need lyrics?(y/N)")
if lyric_needs == "y":
    get_lyrics(songID,title)

#https://music.163.com/#/song?id=536622304 has bug,album cover can't assert into MP3


'''
 	class ClassName(object):
 		"""docstring for ClassName"""
 		def __init__(self, arg):
 			super(ClassName, self).__init__()
 			self.arg = arg
 			
'''
