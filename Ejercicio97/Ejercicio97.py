class Playlist:
    '''A class to represent a music playlist.'''
    def __init__(self, name):
        self.__name = name
        self.songs = []
    def add_song(self, song):
        self.songs.append(song)
        print(f"Added: {song}")
    def remove_song(self, song):
        if song in self.songs:
            self.songs.remove(song)
            print(f"Removed: {song}")
    def show_songs(self):
        print(f"Playlist '{self.__name}':")
        for song in self.songs:
            print(f"- {song}")
            
    def __setattr__(self, name, value):
        if name == "__name__":
            self.__name = value

    
    
my_playlist = Playlist("Favorites")
my_playlist.add_song("Bohemian Rhapsody")
my_playlist.add_song("Stairway to Heaven")
my_playlist.show_songs()
my_playlist.remove_song("Stairway to Heaven")
my_playlist.show_songs()