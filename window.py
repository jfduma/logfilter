from abc import abstractmethod, ABCMeta


class Window(object):
    __metaclass__ = ABCMeta

    def __init__(self, root):
        self.window = None
        self.root = root

    @abstractmethod
    def init_show(self):
        raise NotImplementedError("Must override __init_show")

    def show(self):
        if self.window is None:
            self.window = self.init_show()
            self.window.wm_protocol("WM_DELETE_WINDOW", lambda: self.closeCallback())
        else:
            self.window.focus_set()

    def closeCallback(self):
        self.window.destroy()
        self.window = None

