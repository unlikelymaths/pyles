from data.image import Image


class ImageSection():

    def __init__(self, image, pos = None, size = None):
        self.image = image
        self.reset_data()
        
        if pos is None and size is None:
            self.size = self.image.size
            self.pos = (0,0)
        elif pos is None:
            self.size = size
            self.pos = (self.image.size[0]/2 - self.size[0]/2,
                        self.image.size[1]/2 - self.size[1]/2)
        elif size is None:
            self.pos = pos
            self.size = (self.image.size[0] - self.pos[0],
                         self.image.size[1] - self.pos[1])
        else:
            self.pos = pos
            self.size = size
               
    def reset_data(self):
        self._tex_coords = None
        self._relpos = None
        self._relsize = None
        self._aspect_ratio = None
               
    @property
    def tex_coords(self):
        if self._tex_coords is None:
            self._tex_coords = [self.relpos[0],
                                   1-self.relpos[1], 
                               self.relpos[0]+self.relsize[0],
                                   1-self.relpos[1], 
                               self.relpos[0]+self.relsize[0], 
                                   1-self.relpos[1]-self.relsize[1], 
                               self.relpos[0],                 
                                   1-self.relpos[1]-self.relsize[1]]
        return self._tex_coords
        
    @property
    def texture(self):
        return self.image.texture
        
    @property
    def aspect_ratio(self):
        if self._aspect_ratio is None:
            self._aspect_ratio = self.size[0] / self.size[1]
        return self._aspect_ratio
        
    @property
    def relpos(self):
        if self._relpos is None:
            self._relpos = (self.pos[0] / self.image.size[0], self.pos[1] / self.image.size[1])
        return self._relpos
        
    @property
    def relsize(self):
        if self._relsize is None:
            self._relsize = (self.size[0] / self.image.size[0], self.size[1] / self.image.size[1])
        return self._relsize