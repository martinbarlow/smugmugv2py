from AlbumImage import AlbumImage
from Uri import Uri

class Album(object):
    def __init__(self, album):
        for key in album:
            setattr(self, key.lower(), album[key])
        self.uris = Uri(album["Uris"])

    @classmethod
    def get_album(cls, connection, album_uri):
        return cls(connection.get(album_uri)["Album"])

    def get_images(self, connection):
        ret=[]

        if self.imagecount:
            images = connection.get(self.uris.albumimages)["AlbumImage"]
            for image in images:
                thisimage = AlbumImage(image)
                ret.append(thisimage)

        return ret

    def delete_album(self, connection):
        return connection.delete(self.uri)

    def change_album(self, connection, changes):
        return connection.patch(self.uri, changes)["Response"]["Album"]
