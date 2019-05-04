from PIL import Image as PILImage
from array import array
from kivy.graphics.texture import Texture

class ImageLoadError(IOError):
    pass

class Image():
    def __init__(self, filename, load_now = False):
        self.reset_data()
        self._filename = filename
        if load_now:
            self.texture
        
    def reset_data(self):
        self._filename = None
        self._pil_image = None
        self._texture = None
        self._size = None
        
    @property
    def image(self):
        if self._pil_image is None and self._filename is not None:
            try:
                self._pil_image = PILImage.open(self._filename)
            except OSError:
                filename = self._filename
                self.reset_data()
                raise ImageLoadError('Cannot open image "{}".'.format(filename))
        return self._pil_image
        
    @property
    def texture(self):
        if self._texture is None and self.image is not None:
            # Get rawdata from image
            buf = self.image.getdata()
            
            # Unpack tuples and form array
            buf = [int(val) for triple in buf for val in triple]
            arr = array('B', buf)
            
            # Create a new texture and blit data
            self._texture = Texture.create(size=self.size)
            self._texture.blit_buffer(arr, colorfmt='rgb', bufferfmt='ubyte')
            self._texture.flip_vertical()
        return self._texture
    
    @property
    def size(self):
        if self._size is None and self.image is not None:
            self._size = self.image.size
        return self._size
    
    @property
    def aspect_ratio(self):
        return self.size[0] / self.size[1]
        