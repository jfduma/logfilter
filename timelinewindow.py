import tkinter as tk


class TimeLineWindow:

    def __init__(self, root, time_line):
        self.root = root
        self.time_line = time_line

    def show(self, callback):
        self.callback = callback
        self.window = tk.Toplevel(self.root)
        self.window.title("time line")
        self.window.geometry('280x280+1220+500')
        self.window.wm_protocol("WM_DELETE_WINDOW", lambda: self.closeCallback())

        v = tk.IntVar(0)

        for index in range(len(self.time_line) - 1):
            item = self.time_line[index]
            nextitem = self.time_line[index + 1]
            radio_button = self.addFilePieceRadioButton(item, nextitem, index, v)

    def addFilePieceRadioButton(self, curr, nextitem, index, var):
        startline = curr.line_num
        endline = nextitem.line_num
        radio_button = tk.Radiobutton(self.window,
                                      text="%s--%s" % (curr.start_time, nextitem.start_time),
                                      command=lambda: self.callback(startline, endline),
                                      variable=var, value=index + 1, indicatoron=False)
        radio_button.pack(side='top', fill='x')
        return radio_button

    def closeCallback(self):
        pass