import requests
import base64
import json
import os
import mysql.connector
import string
from urllib.parse import urlencode
import urllib
import config
from SpotifySecrets import spotify_user_id,client_id,client_secret,getToken
from mysql.connector import  errorcode
access_token='BLANK'
global play
playlists = []
tracks = []

class Track(object):
     def __init__(self,name,id,artists,track_number,href):
          self.name=name
          self.id=id
          self.artists=artists
          self.track_number=track_number
          self.href=href

class Playlist(object):
      def __init__(self,name,id,href):
        self.id=id
        self.name=name
        self.href=href

class PlaylistAggregator(object):
    access_token_expires = None
    client_id = None
    client_secret = None

    def __init__(self,client_id,client_secret,spotify_user_id, *args,**kwargs):
         super().__init__(*args,**kwargs) #cancallanyclassinheritingfromitself
         self.client_id=client_id
         self.client_secret=client_secret
         self.user_id=spotify_user_id
        
        
    def spotifyLogin(self):
         global access_token
         access_token=getToken()
    
    def getPlaylists(self):
         headers = {"Authorization": "Bearer " + access_token}
         params = {'limit': '50'}
         getPlaylists=requests.get('https://api.spotify.com/v1/me/playlists',headers=headers,params=params)
         global playlistsJson
         playlistsJson=getPlaylists.json()
         items = playlistsJson['items']
         print ()
         print ("HERE ARE ALL YOUR PLAYLISTS")
         print ()
         for item in items:
           obj = Playlist(item['name'],item['id'],item['href'])
           playlists.append(obj)

    def getSongFeatures(self,trackID):
         #3Nwxgwe88pKBAtw6gxf8JX
         #2Kqkhx3s12R2Vzxtv2loh5
         headers = {"Authorization": "Bearer " + access_token}
         url='https://api.spotify.com/v1/audio-features/' + trackID
         getSong=requests.get(url,headers=headers)
         getSongJson=getSong.json()
         print(getSongJson)
         pass

    def getGenres(self):
         headers = {"Authorization": "Bearer " + access_token}
         params={'limit':'50'}
         url='https://api.spotify.com/v1/browse/categories'
         response=requests.get(url,headers=headers,params=params)
         genres=response.json()
         items=genres['categories']['items']
         for item in items:
             print(item['id']," -- ", item['name'])
         
    def getGenresFromAlbum(self,albumID):
         headers = {"Authorization": "Bearer " + access_token}
         url='https://api.spotify.com/v1/albums/' + albumID
         response=requests.get(url,headers=headers)
         responseJson=response.json()
         #print(responseJson)
         print(responseJson['genres'])
    
    def getSongsMatchingParameters(self):
         headers = {"Authorization": "Bearer " + access_token}
         params={'min_tempo':'160','max_tempo':'175','min_energy':'0.850','seed_genres':['house','edm_dance','techno','instrumnetal','techno'],'seed_artists':['01K8GEMGGxtrQ4xjDmNLPs','5RVfulub05A24HJQ06JObr','5TgQ66WuWkoQ2xYxaSTnVP'],'seed_tracks':['2Kqkhx3s12R2Vzxtv2loh5','21JRqTnNDTiMxzTCvzcfc3','3Nwxgwe88pKBAtw6gxf8JX','7kp2RyfqxTvLSvGHUNshFc']}
         url='https://api.spotify.com/v1/recommendations'
         response=requests.get(url,headers=headers,params=params)
         plistJson=response.json()
         tracks = plistJson['tracks']
         
         for track in tracks:
            print()
            print(track['name'] )
            names=track['artists']
            for name in names:
             print(' ---> ' + name['name'])

    def getAllGenres(self):
         headers={"Authorization" : "Bearer " + access_token}
         params={'limit':'50','offset':'0'}
         url='https://api.spotify.com/v1/browse/categories'
         response=requests.get(url,headers=headers,params=params)
         genresJson=response.json()
         genres=genresJson['categories']['items']
         for genre in genres:
          print(genre['id'] + " - " + genre['name'])

    def getTrack(self,trackID):
        headers = {"Authorization": "Bearer " + access_token}
        url='https://api.spotify.com/v1/tracks/' + trackID
        getTrack=requests.get(url,headers=headers)
        trackJson=getTrack.json()
        print("ALBUM ID = " + trackJson['album']['id'])
        artists=trackJson['artists']
        for artist in artists:
          print(artist['name'])
        print(" - " + trackJson['name'])

    def getSongsFromPlaylist(self,plistName): 
         print ()
         print ("PLAYLIST = "+ plistName )
         print ()
         items=[0]
         offset =0
         i=1
         plist_id=playlistsJson['items']
         while  items:
          try:
               headers = {"Authorization": "Bearer " + access_token}
               params ={'offset' : offset,'limit':'100'}
               items = playlistsJson['items']
               for item in items:
                    if item['name']==plistName:
                         plist_id=item['id']
               url='https://api.spotify.com/v1/playlists/' + plist_id + '/tracks'
               getPlaylist=requests.get(url,headers=headers,params=params)
               requests.raise_for_status()
               playlistJson=getPlaylist.json()
               items = playlistJson['items']
               for item in items:
                    print(f"Track - {i}: ")
                    artists=item['track']['artists']
                    name=''
                    for artist in artists:
                         name = name + artist['name'] + " "
                    print(name, "- " + item['track']['name'], " " + item['track']['id'])
                    i=i+1
          except requests.exceptions.HTTPError as err:
               print(err.response.text)
          except requests.exceptions.ConnectionError as err:
               print(err.response.text)
          offset=offset +100

    def updatePlaylists(self):
         #Need to account for playlists deleted from spotify side
          for playlist in playlists:
               
               query="SELECT EXISTS(SELECT id FROM playlists WHERE id = %s)"
               mycursor.execute(query,(playlist.id,))
               results=mycursor.fetchone()
               count=results[0]
               if count == 0:
                  #print("HREF ",playlist.href,"NAME ",playlist.name)
                  mycursor.execute("INSERT INTO playlists (id,name,href) VALUES (%s,%s,%s)",(playlist.id,playlist.name,playlist.href))
                  db.commit()
          print("------Playlists Updated--------")    
if __name__ == "__main__":
    try:
       db = mysql.connector.connect(
         host="localhost",user="mikemuponda",passwd=base64.b64decode(config.MYSQLpassword).decode("utf-8"),
         database="test",port=3306 ,auth_plugin='mysql_native_password',charset = 'utf8mb4'
       )
       if db.is_connected()==True:
            print ("connected to " + db.database)
            mycursor = db.cursor()#(dictionary=True)
            spotify=PlaylistAggregator(client_id,client_secret,spotify_user_id)
            spotify.spotifyLogin()
            #spotify.getPlaylists()
            #spotify.updatePlaylists()
            spotify.getSongsFromPlaylist("Summatime jawns")
            #spotify.getSongFeatures('2Kqkhx3s12R2Vzxtv2loh5')
            print()
            #spotify.getSongFeatures('2Kqkhx3s12R2Vzxtv2loh5')
            #spotify.getSongsMatchingParameters()
            #spotify.getGenres()
            #spotify.getTrack('3Nwxgwe88pKBAtw6gxf8JX')
            #spotify.getGenresFromAlbum('1ATL5GLyefJaxhQzSPVrLX')
            #spotify.getAllGenres()

    except mysql.connector.Error as err:
         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR :
              print("Username or password incorrect")
         elif err.errno ==errorcode.ER_BAD_DB_ERROR :
               print("database does not exist")
         else :
               print("OTHER ERROR",err)
    finally :
         db.close()
         print("connection terminated")
    