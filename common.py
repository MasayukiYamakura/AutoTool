# common.py
import streamlit as st
import extra_streamlit_components as stx


#ログインの確認
def check_login():
	value = stx.CookieManager().get(cookie='some_cookie_name')
	# if value != []:
	if value == None:
		st.warning('ログインして下さい	', icon="⚠")
		st.stop()