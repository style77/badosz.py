from io import BytesIO


class File(object):
    def __init__(self, request_data, request_headers, *, filename="nothing"):
        self.r_data = request_data
        self.r_headers = request_headers
        self.fn = filename
        self.formats_map = {
                    "image/png": "png",
                    "image/gif": "gif",
                    "image/jpeg": "jpg",
                    "image/webp": "webp",
                    "video/mp4": "mp4",
                    "video/webm": "webm"
                    }

    @property
    def type(self):
        type_ = self.r_headers['Content-Type']
        return type_

    def get_discord_file(self):
        try:
            import discord
        except ImportError:
            raise Exception("To use 'get_discord_file' you need to have discord package.")

        type_ = self.type
        image = BytesIO(self.r_data)
        return discord.File(fp=image, filename=f"{self.fn}.{self.formats_map[type_]}")

    def get_file(self):
        image = BytesIO(self.r_data)
        return image
