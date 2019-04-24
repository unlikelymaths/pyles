
class GenericSetting():
    def __init__(self, name = ''):
        self.name = name


class FilePathSetting(GenericSetting):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)