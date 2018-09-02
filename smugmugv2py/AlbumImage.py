from iso8601 import parse_date
from Uri import Uri

class AlbumImage(object):
    def __init__(self, image):
            for key in image:
                setattr(self, key.lower(), image[key])
            self.uris = Uri(image["Uris"])
            self.last_updated = parse_date(image["LastUpdated"]).replace(tzinfo=None)

    @classmethod
    def get_album_image(cls, connection, image_uri):
        return cls(connection.get(image_uri)["Image"])

    def delete_album_image(self, connection):
        return connection.delete(self.uri)

    def change_album_image(self, connection, changes):
        return AlbumImage(connection.patch(self.uri, changes)["Response"]["Image"])
