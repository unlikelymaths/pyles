import sys
import os

def widget_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    real_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))
    base_path = getattr(sys, '_MEIPASS', real_path)
    return os.path.join(base_path, relative_path)