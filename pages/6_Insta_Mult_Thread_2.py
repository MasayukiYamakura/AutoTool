# import threading
# import time
# import streamlit as st

# def process():
#     st.write('Process Start')
#     time.sleep(3)
#     st.write('Process End')


# press_button = st.button("自動フォロー開始")

# if press_button:
#     threadA = threading.Thread(target=process)
#     threadA.start()
#     time.sleep(5)
#     threadA.join()
#     st.write('Main End')

import asyncio

async def main():
    st.write('Hello ...')
    await asyncio.sleep(1)
    st.write('... World!')

press_button = st.button("自動フォロー開始")

if press_button:
    asyncio.run(main())