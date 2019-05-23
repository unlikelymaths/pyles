import PIL
from array import array
from kivy.graphics.texture import Texture 

class ImageLoadError(IOError):
    pass

class Image():
    def __init__(self, filename):
        self._arr = None
        self._bytes = None
        self._texture = None
        self._mode = 'RGB'
        self.size = None
        self.aspect_ratio = None
        self.load_image(filename)
                
    def load_image(self, filename):
        try:
        #Load image file
            pil_image = PIL.Image.open(filename)
            pil_image = pil_image.convert(self._mode)
            # Get rawdata from image
            self._bytes = pil_image.tobytes()
            buf = pil_image.getdata()
            # Unpack tuples and form array
            buf = [int(val) for triple in buf for val in triple]
            self._arr = array('B', buf)
            # Set size
            self.size = pil_image.size
            self.aspect_ratio = self.size[0] / self.size[1]
        except OSError:
            self._arr = None
            raise ImageLoadError('Cannot open image "{}".'.format(filename))
    
    def save(self, file_path):
        self.image.save(file_path)
    
    @property
    def image(self):
        return PIL.Image.frombytes(self._mode, self.size, self._bytes)
    
    @property
    def texture(self):
        if self._texture is None and self._arr is not None:
            # Create a new texture and blit data
            self._texture = Texture.create(size=self.size)
            self._texture.blit_buffer(self._arr, colorfmt='rgb', bufferfmt='ubyte')
            self._texture.flip_vertical()
        return self._texture