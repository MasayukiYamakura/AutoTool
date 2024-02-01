import threading
import time

def process():
    st.write('Process Start')
    time.sleep(3)
    st.write('Process End')


press_button = st.button("自動フォロー開始")

if press_button:
    threadA = threading.Thread(target=process)
    threadA.start()
    time.sleep(1)
    threadA.join()
    st.write('Main End')