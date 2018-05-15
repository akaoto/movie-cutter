import os
import cv2
import fire
from PIL import Image


class Video(object):
    """
    Wrapper class of cv2.VideoCapture.
    """

    def __init__(self, fname):
        self._vc = cv2.VideoCapture(fname)
        self.width = int(self._vc.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self._vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_count = int(self._vc.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self._vc.get(cv2.CAP_PROP_FPS)
        self.interval = 1 / self.fps

    def read(self):
        return self._vc.read()


class MovieCutter(object):

    def __init__(self, fname):
        self._fname = os.path.splitext(
            os.path.basename(fname)
        )[0]
        self._video = Video(fname)

    def info(self):
        """
        Describe information of specified file.
        """

        s = f"""width : {self._video.width}
height : {self._video.height}
count : {self._video.frame_count}
fps : {self._video.fps}
"""
        return s

    def cut(self, interval, cut_range=None):
        """
        Cut the movie.

        Args:
            interval (float): Interval of saved frames.
            cut_range (array of int), optional: Cut out range of saved frames.

        Returns:
            str: Message to finish, 'Finished'.
        """

        step = interval // self._video.interval
        for f in range(0, self._video.frame_count):
            successed, img_array = self._video.read()
            if not successed:
                raise RuntimeError('Video read error')

            i, mod = divmod(f, step)
            if not mod:
                if cut_range:
                    c = cut_range
                    img_array = img_array[c[0]:c[1], c[2]:c[3]]
                img = Image.fromarray(img_array)
                fname = f'{self._fname}_{interval * i}.png'
                img.save(fname)
                print(f'Written {fname}')

        return 'Finished.'


if __name__ == '__main__':
    fire.Fire(MovieCutter)
