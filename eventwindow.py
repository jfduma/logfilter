import tkinter as tk

from filterutils import Condition, EVENT_TAG_MAP, EVENT_MARK


class EventSelectWindow:

    def __init__(self, root, callback):
        self.condition_dict = {}
        self.root = root
        self.callback = callback
        self.window = tk.Toplevel(root)
        self.window.title("事件窗口")
        self.window.geometry('280x320+1220+100')
        self.window.wm_protocol("WM_DELETE_WINDOW", lambda: self.closeCallback())

        first_frame = tk.LabelFrame(self.window, relief='raised')
        first_frame.pack(side='top', fill='x')

        # 执行过滤按钮
        btn_add_condition = tk.Button(first_frame, text="done",
                                      command=lambda: self.callback(self.condition_dict.values()))
        btn_add_condition.pack(side='left')

        self.initConditions()

    def show(self):
        self.window.focus_set()

    def initConditions(self):
        for key in list(EVENT_TAG_MAP.keys()):
            condition = Condition(EVENT_TAG_MAP[key])
            condition.mode = 1
            condition.addIncludeKey('\\[' + EVENT_MARK + key + '\\]')
            self.addCondition(condition)

    def addCondition(self, condition):
        cb = tk.Checkbutton(self.window, text=condition.name, indicatoron=False, variable=condition.available)
        cb.pack(side='top', fill='x')
        self.condition_dict[cb] = condition

    def closeCallback(self):
        self.callback([])
        self.window.destroy()
