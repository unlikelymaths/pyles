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
            self._load_pil_image()
            self._pil_to_texture()
        
    def reset_data(self):
        self._filename = None
        self._pil_image = None
        self._texture = None
        self._size = None
        
    @property
    def texture(self):
        self._load_pil_image()
        if self._pil_image is not None and self._texture is None:
            self._pil_to_texture()
        return self._texture
    
    @property
    def size(self):
        self._load_pil_image()
        return self._size
    
    @property
    def aspect_ratio(self):
        self._load_pil_image()
        return self._size[0] / self._size[1]
        
    def _load_pil_image(self):
        if self._pil_image is None and self._filename is not None:
            try:
                self._pil_image = PILImage.open(self._filename)
            except OSError:
                filename = self._filename
                self.reset_data()
                raise ImageLoadError('Cannot open image "{}".'.format(filename))
            self._size = self._pil_image.size
    
    def _pil_to_texture(self):
        # Return if data is missing
        if self._pil_image is None:
            return
          
        # Get rawdata from image
        buf = self._pil_image.getdata()
        
        # Unpack tuples and form array
        buf = [int(val) for triple in buf for val in triple]
        arr = array('B', buf)
        
        # Create a new texture and blit data
        self._texture = Texture.create(size=self._size)
        self._texture.blit_buffer(arr, colorfmt='rgb', bufferfmt='ubyte')
        self._texture.flip_vertical()