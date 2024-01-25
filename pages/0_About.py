import streamlit as st
import common

#共通チェック
common.check_login()

st.title("About this app")

st.markdown('''
## このAppについて
これはInstagram・X・Yayの自動ツールになります。

## 自己紹介

M.Yamakura

[@toichi_t](https://twitter.com/yoichi_t)
''')

# *** sidebar
st.sidebar.title('About')
st.sidebar.markdown("""
このAppについて
""")
