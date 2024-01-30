# main.py

import streamlit as st
import streamlit_authenticator as stauth
import yaml

# ファイル設置場所 Local環境
# Config_File = '../D160_Login/config.yaml'
# ファイル設置場所 本番環境
Config_File = './config.yaml'

with open(Config_File) as file:
	config = yaml.load(file, Loader=yaml.SafeLoader)

authenticator = stauth.Authenticate(
	config['credentials'],
	config['cookie']['name'],
	config['cookie']['key'],
	config['cookie']['expiry_days'],
	config['preauthorized'],
)

name, authentication_status, username = authenticator.login("Login", "main")



if 'authentication_status' not in st.session_state:
	st.session_state['authentication_status'] = None

if st.session_state["authentication_status"]:
	authenticator.logout('Logout', 'main')
	st.write(f'ログインに成功しました')
	# ここにログイン後の処理を書く。
	# add start 
	st.title("Multipage Sample")
	st.header('こんにちは 世界')

	st.markdown('''
	こんにちは！

	これはStreamlitMultiPageAppのテストです。
	Multipageについては、下記サイトを参照してください。

	- https://docs.streamlit.io/library/get-started/multipage-apps
	- https://blog.streamlit.io/introducing-multipage-apps/
	''')


	# *** sidebar
	st.sidebar.title('home')
	# st.sidebar.image('asset/neko.png', use_column_width=True)
# add end
elif st.session_state["authentication_status"] is False:
	st.error('ユーザ名またはパスワードが間違っています')
elif st.session_state["authentication_status"] is None:
	st.warning('ユーザ名やパスワードを入力してください')
