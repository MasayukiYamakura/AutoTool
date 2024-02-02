import streamlit as st
import threading
import time
import sys
 
def func():
    while True:
        time.sleep(0.5)
        print("Thread alive, and it won't die on program termination")


press_button1 = st.button("自動フォロー開始")


if press_button1:
    t1 = threading.Thread(target=func)
    t1.start()
    time.sleep(2)
    sys.exit()

