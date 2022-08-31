import subprocess
import tkinter as tk
from tkinter import ttk


class SimulateSignalWindow:

    def __init__(self, root):
        self.root = root
        self.org_condition = None
        self.tag = None
        self.simulateEnable = False

        self.intent_simulate_signal = "com.bytedance.auto.sceneengine.INTENT_SIMULATE_SIGNAL"
        self.intent_simulate_enable = "com.bytedance.auto.sceneengine.INTENT_ENABLE_SIMULATE"
        self.values_map = \
            {
                '天气详情': 'signal_weather_detail',
                'BBB': 'bbb',
                'CCC': 'ccc',
                'DDD': 'ddd'
            }

    def show(self):
        self.top = tk.Toplevel(self.root)
        self.top.title("信号模拟")
        self.top.geometry('530x380+400+200')

        frame_first = tk.Frame(self.top)
        frame_first.pack(side='top', fill='x')

        self.btn_simulate_enalbe = tk.Button(frame_first, text='开启模拟', command=self.onEnableSimulateClick)
        self.btn_simulate_enalbe.pack(side='left')

        frame_second = tk.Frame(self.top)
        frame_second.pack(side='top', fill='x')

        self.combo_text = tk.StringVar()
        self.combo_list = ttk.Combobox(frame_second, textvariable=self.combo_text,
                                       values=list(self.values_map.keys()),
                                       state="readonly", width=20)
        self.combo_list.pack(side='left')
        # self.combo_list.bind('<<ComboboxSelected>>', self.onChoose)

        self.btn_send = tk.Button(frame_second, text='发送', command=self.onSendClick)
        self.btn_send.pack(side='right')

        self.json_text = tk.Text(self.top, width=10, height=5, font=('Menlo Regular', 14), wrap='char', spacing1=5)
        self.json_text.pack(side='top', fill='x')

        self.result_text = tk.Text(self.top, width=10, height=10, font=('Menlo Regular', 14), wrap='char', spacing1=5)
        self.result_text.pack(side='top', fill='x')

    # def onChoose(self, event):
    #     print("value = " + self.combo_text.get())

    def onSendClick(self):
        key = self.combo_text.get()
        name = self.values_map[key]
        text = self.json_text.get(0.0, tk.END)
        value = text.replace(r'"', r'\"')
        cmd = 'adb shell am broadcast -a "{}" -e "name" "{}" -e "value" \'{}\'' \
            .format(self.intent_simulate_signal, name, value)
        self.sendBroadcast(cmd)

    def onEnableSimulateClick(self):
        enable = 'off' if self.simulateEnable else 'on'
        text = "开启模拟" if self.simulateEnable else "关闭模拟"

        self.btn_simulate_enalbe.config(text=text)
        cmd = 'adb shell am broadcast -a "{}" -e "value" "{}"'.format(self.intent_simulate_enable, enable)
        self.sendBroadcast(cmd)

    def sendBroadcast(self, cmd):
        logpip = subprocess.Popen(
            args=cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)
        with logpip:
            for line in logpip.stderr:
                self.result_text.insert(0.0, line)

            for line in logpip.stdout:
                self.result_text.insert(0.0, line)
