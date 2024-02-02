import threading
import time
import streamlit as st
 
def run(stop):
    while True:
        st.write('thread running')
        if stop():
                break
                 
def main():
        stop_threads = False
        t1 = threading.Thread(target = run, args =(lambda : stop_threads, ))
        t1.start()
        time.sleep(1)
        stop_threads = True
        t1.join()
        st.write('thread killed')

press_button1 = st.button("自動フォロー開始")

if press_button1:
    main()
