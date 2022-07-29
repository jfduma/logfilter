import threading
import re
import subprocess
from queue import Queue
import chardet


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

        command = "adb logcat -c; adb logcat -v threadtime"  # 具体命令

        logpip = subprocess.Popen(
            args=command,
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)

        # 实时监控并过滤每一行生成的日志里的关键字
        print("Logcat catching and filtering...")
        with logpip:
            while self.running:
                line = logpip.stdout.readline()
                encode_type = chardet.detect(line)
                line = line.decode(encode_type['encoding'])

                condition_list = self.condition_list
                success = True
                for condition in condition_list:
                    if condition.available.get() == 0:
                        continue
                    success = True
                    incpatt = condition.getIncludeKeys()
                    if incpatt is not None:
                        for key in incpatt:
                            if 0 == len(re.findall(key, line, re.IGNORECASE)):
                                success = False
                                break

                    if success:
                        excpatt = condition.getExcludeKeys()
                        if excpatt is not None:
                            for key in excpatt:
                                if len(re.findall(key, line, re.IGNORECASE)) > 0:
                                    success = False
                                    break
                    # conditionList中满足其中任意一个condition即可
                    if success:
                        break

                if success:
                    self.callback(line)

            print("stop real time log catching")
