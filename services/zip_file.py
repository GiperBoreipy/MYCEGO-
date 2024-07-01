from dataclasses import dataclass
from zipfile import ZipFile
from io import BytesIO

from PIL import Image


@dataclass
class ZipService:
    zip_file: ZipFile
    folder_prefix: str

    def get_folders(self) -> tuple[str]:
        folders = set([
            file.split("/")[1] for file in self.zip_file.namelist()
        ])
        return tuple([i for i in folders if i])

    def get_photos(self, folders: list[str]) -> tuple[BytesIO]:
        photos = []

        for photo in self.zip_file.namelist():
            for dir_name in folders:
                if photo.startswith(self.folder_prefix + dir_name):
                    photo_bytes = BytesIO(self.zip_file.read(photo))

                    if len(photo_bytes.read()) == 0:
                        continue

                    photos.append(Image.open(photo_bytes))

        return tuple(photos)
