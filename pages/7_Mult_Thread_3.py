import sys
import time
import threading
import trace


class KThread(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == "call":
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == "line":
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


def exfu():
    print("The function begins")
    for i in range(1, 100):
        print(i)
        time.sleep(0.2)
    print("The function ends")

press_button1 = st.button("自動フォロー開始")

press_button2 = st.button("自動フォロー終了")

if press_button1:
    x = KThread(target=exfu)
    x.start()
    time.sleep(1)

if press_button2:
    x.kill()



