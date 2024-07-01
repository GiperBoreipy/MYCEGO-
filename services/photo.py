import math

from PIL import Image


class PhotoService:
    def __init__(
            self,
            photos: tuple[Image]
    ):
        self.photos = photos

        self.h_and_w = math.ceil(len(photos) ** 0.5)
        self.size = self.photos[0].height

    def get_base_photo(self) -> Image:
        return Image.new("RGB", ((2 * self.h_and_w + 1) * self.size, (2 * self.h_and_w + 1) * self.size), (255, 255, 255))

    def get_tif_collage(self) -> Image:
        base_photo = self.get_base_photo()

        photos_i = 0

        flag = False
        for i in range(1, 2 * self.h_and_w + 1, 2):
            for j in range(1, 2 * self.h_and_w + 1, 2):
                if photos_i > len(self.photos) - 1:
                    flag = True
                    break

                base_photo.paste(self.photos[photos_i], (i * self.size, j * self.size))
                photos_i += 1

            if flag:
                break

        return base_photo
