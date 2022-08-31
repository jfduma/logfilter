import threading
import re
import subprocess
from queue import Queue
import chardet

from filterutils import filterText


class RealTimeLogFilter:

    def __init__(self, callback):
        self.callback = callback
        self.condition_list = []
        self.queue = Queue()
        self.running = True

    def setConditions(self, conditions):
        self.condition_list = conditions

    def stop(self):
        self.running = False

    def start(self):
        thread = threading.Thread(name='adblog', target=self.start_internal)
        thread.start()

    def start_internal(self):
        # 开始执行adb命令
        # subprocess.call("adb shell logcat -c", shell=True)

        # command = "adb logcat -c; adb logcat -v threadtime"  # 具体命令
        command = "/Users/jiangfeng/Library/Android/sdk/platform-tools/adb devices"

        logpip = subprocess.Popen(
            args=command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)

        # 实时监控并过滤每一行生成的日志里的关键字
        print("Logcat catching and filtering...")

        with logpip:
            while self.running:
                for line in logpip.stderr:
                    print(line)

                line = logpip.stdout.readline()
                if len(line) > 0:
                    print("Logcat: " + str(len(line)))
                    encode_type = chardet.detect(line)
                    if encode_type['encoding'] is not None:
                        line = line.decode(encode_type['encoding'])
                        condition_list = self.condition_list
                        result = filterText(line, condition_list)
                        if result is not None:
                            self.callback(result)

            print("stop real time log catching")
