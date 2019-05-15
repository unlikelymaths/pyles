if __name__ == '__main__': # to avoid new window with a new process
    import multiprocessing
    multiprocessing.freeze_support()
    
    from kivy.config import Config
    Config.set('input', 'mouse', 'mouse,disable_multitouch')
    
    from app import Pyles
    Pyles().run()