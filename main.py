import requests

from zipfile import ZipFile
import io
import json

from services import PhotoService, ZipService

from exceptions import FolderNotFound, DiskNotFound


BASE_URL = "https://cloud-api.yandex.net/v1/disk/public/resources/download"
DISK_URL = "https://disk.yandex.ru/d/V47MEP5hZ3U1kg"

FOLDER_PREFIX = "Для тестового/"


def get_download_link() -> str:
    request_url = BASE_URL + "?public_key=" + DISK_URL

    response = requests.get(request_url)

    if response.status_code != 200:
        raise DiskNotFound("Ресурс не найден.")

    link = response.json()["href"]

    return link


def get_zip_instance(link_to_download: str) -> ZipFile:
    download = requests.get(link_to_download)

    zip_file = ZipFile(io.BytesIO(download.content))

    return zip_file


if __name__ == '__main__':
    dir_names = json.loads(input("Введите название папок в виде списка:\n"))

    download_link = get_download_link()

    zip_file = get_zip_instance(download_link)

    zip_service = ZipService(zip_file, FOLDER_PREFIX)

    folders = zip_service.get_folders()

    for dir_name in dir_names:
        if dir_name not in folders:
            raise FolderNotFound(f"Такой папки нет на диске: {dir_name}")

    photos = zip_service.get_photos(dir_names)

    photo_service = PhotoService(photos)

    result = photo_service.get_tif_collage()

    result.save("result.tif")

    print("Результат сохранён в директории проекта!")
