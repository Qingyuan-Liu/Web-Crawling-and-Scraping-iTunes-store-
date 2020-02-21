#########################################
##### Name:Qingyuan Liu             #####
##### Uniqname: qyyf                #####
#########################################
import requests
import json
import webbrowser


class Media:
    '''Media
    Attributes
    ----------
    title : string
        The title of a media 
    author : string
        The author's name of the media
    realease_year : string
        The release_year of the media
    url : string
        The url for the media which we will need to open later
    json : dictionary
        The dictionary which contains the information about this media
    '''
    def __init__(self, title="No Title", author="No Author",\
        release_year="No Release Year",\
         url="No URL", json=None):      
      
        if json:
            if "trackName" in json:
                self.title= json["trackName"]
            else:
                self.title = json["collectionName"]
            self.author = json["artistName"]
            self.release_year=json["releaseDate"][0:4]
            if "trackViewUrl" in json:      
                self.url=json["trackViewUrl"]
            else:
                self.url=json["collectionViewUrl"]
        else:
            self.title=title
            self.author=author
            self.release_year=release_year
            self.url=url

    def info(self):
        '''Get the information about the media.

        Parameters
        ----------
        none

        Returns
        -------
        str
            The information of the media
        '''
        return self.title+" by "+self.author+" ("+str(self.release_year)+")"
    
    def length(self):
        '''Get the length of the media.

        Parameters
        ----------
        none

        Returns
        -------
        integer
            The length of the media
        '''
        return 0


class Song(Media):
    '''Song
    Attributes
    ----------
    title : string
        The title of a song 
    author : string
        The author's name of the song
    realease_year : string
        The release_year of the song
    url : string
        The url for the song which we will need to open later
    Album: string
        The album which contains this song
    genre : string
        The genre of the song
    track_length : integer
        The length of the song
    json : dictionary
        The dictionary which contains the information about this song
    '''
    
    def __init__(self, title="No Title", author="No Author",\
                    release_year="No Release Year",\
                    url="No URL", album="No Album",\
                    genre="No Genre", track_length=0, json=None):

        super().__init__(title, author, release_year, url, json)

        if json:
            self.album=json["collectionName"]
            self.genre=json["primaryGenreName"]
            self.track_length=json["trackTimeMillis"]
        else:
            self.album=album
            self.genre=genre
            self.track_length=track_length
         
    def info(self):
        '''Get the information about the song.

        Parameters
        ----------
        none

        Returns
        -------
        str
            The information of the song
        '''
        return super().info()+" ["+self.genre+"]"
    
    def length(self):
        '''Get the length of the song.

        Parameters
        ----------
        none

        Returns
        -------
        integer
            The length of the song
        '''
        return round(self.track_length/1000.0)


class Movie(Media):
    '''Movie
    Attributes
    ----------
    title : string
        The title of a movie 
    author : string
        The author's name of the movie
    realease_year : string
        The release_year of the movie
    url : string
        The url for the movie which we will need to open later
    rating : string
        The rating of the movie
    movie_length : integer
        The length of the movie
    json : dictionary
        The dictionary which contains the information about this movie
    '''
    
    def __init__(self, title="No Title", author="No Author",\
                    release_year="No Release Year",\
                    url="No URL",\
                    rating="No Rating",movie_length=0, json=None):
        super().__init__(title, author, release_year, url,json)
        if json:
            self.rating=json["contentAdvisoryRating"]
            self.movie_length=json["trackTimeMillis"]
        else:
            self.rating=rating
            self.movie_length=movie_length
            
    def info(self):
        '''Get the information about the movie.

        Parameters
        ----------
        none

        Returns
        -------
        str
            The information of the movie
        '''
        return super().info()+" ["+self.rating+"]"

    def length(self):
        '''Get the length of the movie.

        Parameters
        ----------
        none

        Returns
        -------
        integer
            The length of the movie
        '''
        return round(self.movie_length/60000.0)




# Other classes, functions, etc. should go here
                
def main():
    ''' Enter the name of the author,
        it will print the work of the author. 
        Or enter the number of the work listed in the media_list,
        the browser will pop out the content about that song/movie/
        other media.
    '''
    item=input('Enter a search term, or \"exit\" to quit:')
    while True:
        if item!="exit":
            URL="https://itunes.apple.com/search?term="+item
            resp=requests.get(URL)
            results_object=resp.json()
            media_result=results_object["results"]
            count=0
            o_media=[]
            s_media=[]
            m_media=[]
            total_media=[]
            if media_result:
                for p in media_result:
                    if "kind" not in p:
                        other=Media(json=p)
                        o_media.append(other)
                    elif p["kind"]=="song":
                        s=Song(json=p)
                        s_media.append(s)
                    elif p["kind"]=="feature-movie":
                        m=Movie(json=p)
                        m_media.append(m)
                if s_media !=[]:         
                    print("\n")
                    print("SONGS")
                    for list_s in s_media:                    
                        count=count+1
                        print(str(count)+" "+list_s.info())
                if m_media !=[]:
                    print("\n")
                    print("MOVIES")
                    for list_m in m_media:
                        count=count+1
                        print(str(count)+" "+list_m.info())
                if o_media !=[]:
                    print("\n")
                    print("OTHER MEDIA")
                    for list_o in o_media:
                        count=count+1
                        print(str(count)+" "+list_o.info())     
                        
            else:
                item=input('Enter another search term, or \"exit\" to quit:')
                continue
         
            
            while True:
                number=input("\nEnter a number for more info,"+ 
                             "or another search term,or exit:")
                if number.isdigit() == False:
                    item=number
                    break
                elif number.isnumeric and int(number)<=count and int(number)>0:
                    total_media.extend(s_media)
                    total_media.extend(m_media)
                    total_media.extend(o_media)  
                    print("\nLauching\n"+total_media[int(number)-1].url+
                          "\nin web browser...\n")
                    webbrowser.open(total_media[int(number)-1].url)
                else:
                    print("\nPlease enter the valid number or search term!")
                    continue
        else:
            print("\nBye!")
            break





if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here
    main()
