import subprocess
import tkinter as tk
from tkinter import ttk

from window import Window


class SimulateSignalWindow(Window):

    def __init__(self, root):
        Window.__init__(self, root)
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
        self.action_map = \
            {
                '空调开': 'adb shell am broadcast -a "%s" -e "name" "%s" -e "value" %s'
                       % (self.intent_simulate_signal, 'signal_ac_power', '\'{\\"value\\"=\\"on\\"}\''),
                '空调AC开': 'adb shell am broadcast -a "%s" -e "name" "%s" -e "value" %s'
                         % (self.intent_simulate_signal, 'signal_ac_state', '\'{\\"value\\"=\\"on\\"}\''),
                '车门上锁': 'adb shell am broadcast -a "%s" -e "name" "%s" -e "value" %s'
                        % (self.intent_simulate_signal, 'signal_door_lock', '\'\\[\\"locked\\",\\"locked\\"\\]\''),
                'shut_down': 'adb shell am broadcast -a "%s" -e "name" "%s" -e "value" %s'
                             % (self.intent_simulate_signal, 'signal_key_power_state',
                                '\'{\\"value\\"=\\"shut_down\\"}\''),
                'power_on': 'adb shell am broadcast -a "%s" -e "name" "%s" -e "value" %s'
                            % (self.intent_simulate_signal, 'signal_key_power_state',
                               '\'{\\"value\\"=\\"power_on\\"}\''),
                'start_up': 'adb shell am broadcast -a "%s" -e "name" "%s" -e "value" %s'
                            % (self.intent_simulate_signal, 'signal_key_power_state',
                               '\'{\\"value\\"=\\"start_up\\"}\''),
                'rank': 'adb shell am broadcast -a "%s" -e "name" "%s" -e "value" %s'
                        % (self.intent_simulate_signal, 'signal_key_power_state',
                           '\'{\\"value\\"=\\"rank\\"}\''),
            }

    def init_show(self):
        window = tk.Toplevel(self.root)
        window.title("信号模拟")
        window.geometry('530x380+400+200')

        frame_first = tk.Frame(window)
        frame_first.pack(side='top', fill='x')

        tk.Button(frame_first, text='模拟页面', command=lambda: self.sendBroadcast(
            'adb shell am start -n "com.bytedance.auto.sceneengine/.debug.MainActivity"')).pack(side='left')
        tk.Button(frame_first, text='开启模拟', command=lambda: self.sendBroadcast(
            'adb shell am broadcast -a "%s" -e "value" "on"' % self.intent_simulate_enable)).pack(side='left')
        tk.Button(frame_first, text='关闭模拟', command=lambda: self.sendBroadcast(
            'adb shell am broadcast -a "%s" -e "value" "off"' % self.intent_simulate_enable)).pack(side='left')

        frame_second = tk.Frame(window)
        frame_second.pack(side='top', fill='x')

        self.combo_text = tk.StringVar()
        self.combo_list = ttk.Combobox(frame_second, textvariable=self.combo_text,
                                       values=list(self.values_map.keys()),
                                       state="readonly", width=20)

        self.combo_list.pack(side='left')
        # self.combo_list.bind('<<ComboboxSelected>>', self.onChoose)

        self.btn_send = tk.Button(frame_second, text='发送', command=self.onSendClick)
        self.btn_send.pack(side='right')

        # self.json_text = tk.Text(self.top, width=10, height=5, font=('Menlo Regular', 14), wrap='char', spacing1=5)
        # self.json_text.pack(side='top', fill='x')

        # 容纳信号模拟按钮的frame
        self.btn_frame = tk.LabelFrame(window, text="信号模拟")
        self.btn_frame.pack(side='top', fill='x')

        # 添加信号模拟按钮
        column_count = 4
        column = 0
        row = 0
        for name in self.action_map.keys():
            cmd = self.action_map[name]
            self.addSimulateBtn(self.btn_frame, name, cmd, column, row)
            column += 1
            if column_count == column:
                column = 0
                row += 1

        # 输出模拟指令结果的文本框
        self.result_text = tk.Text(window, width=10, height=10, font=('Menlo Regular', 14), wrap='char', spacing1=5)
        self.result_text.pack(side='top', fill='x')
        return window

    # def onChoose(self, event):
    #     print("value = " + self.combo_text.get())

    def addSimulateBtn(self, frame, name, cmd, column, row):
        tk.Button(frame, text=name, command=lambda: self.sendBroadcast(cmd)).grid(column=column, row=row)

    def onSendClick(self):
        key = self.combo_text.get()
        name = self.values_map[key]
        text = ""  # self.json_text.get(0.0, tk.END)
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
        print('sendBroadcast: %s' % cmd)
        self.result_text.delete(0.0, tk.END)
        self.result_text.insert(tk.END, cmd + '\n------------------')
        logpip = subprocess.Popen(
            args=cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)
        with logpip:
            for line in logpip.stderr:
                self.result_text.insert(tk.END, line)

            self.result_text.insert(tk.END, '\n')

            for line in logpip.stdout:
                self.result_text.insert(tk.END, line)
