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

# import streamlit as st
# import asyncio

# async def main():
#     for j in range(1,10):
#         st.write('Hello ...' + str(j))
#         await asyncio.sleep(3)
#         st.write('... World!')
#         await asyncio.sleep(1)

# press_button = st.button("自動フォロー開始")

# press_button2 = st.button("自動フォロー終了")

# if press_button:
#     asyncio.run(main())

import streamlit as st
import asyncio
import os
path = 'foo.txt'


# async def my_task():
#     # 非同期タスクの実装
#     for j in range(1,10):
#         try:
#             while True:
#                 await asyncio.sleep(1)
#                 st.write("タスク実行中")
#         except asyncio.CancelledError:
#             st.write("タスクがキャンセルされました")
async def my_task():
    # ファイル作成処理
    f = open(path, 'w')
    f.write('')  
    f.close()
    is_file = os.path.isfile(path)
    # 非同期タスクの実装
    for j in range(1,10):
        if is_file:
            await asyncio.sleep(1)
            st.write("タスク実行中")
        else:
            st.write("タスクがキャンセルされました")
            break




async def main():
    task = asyncio.create_task(my_task())  # 非同期タスクを作成
    await asyncio.sleep(10)  # 3秒待機
    # task.cancel()  # タスクをキャンセル
    

async def taskcancel():
    os.remove(path)

press_button1 = st.button("自動フォロー開始")

press_button2 = st.button("自動フォロー終了")

if press_button1:
    asyncio.run(main())

if press_button2:
    asyncio.run(taskcancel())
