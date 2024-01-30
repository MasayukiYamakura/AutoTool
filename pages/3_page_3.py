# coding:utf-8

# 必要なパッケージのインポート
import streamlit as st
import time
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome import service as fs
from selenium.webdriver import ChromeOptions
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.common.by import By

# タイトルを設定
st.title("Instagramフォローアプリ")

Instagram_Id = st.text_input('Instagram ID', placeholder='Instagram ID', max_chars=50, help='電話番号かメールアドレスかID')

Instagram_Password = st.text_input('Instagram Password', placeholder='Instagram Password', max_chars=50)

Follower_List_Id =  st.text_input('Follower_List_Id', placeholder='Follower_List_Id', max_chars=50, help='例:hina_k_1019')

Loop_Counts = st.slider('フォローする件数', 0, 200, 25)

# ボタンを作成(このボタンをアプリ上で押すと"if press_button:"より下の部分が実行される)
press_button = st.button("スクレイピング開始")



if press_button:

	# ドライバのオプション
	options = ChromeOptions()

	# option設定を追加（設定する理由はメモリの削減）
	options.add_argument("--headless")
	options.add_argument('--disable-gpu')
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')

	# webdriver_managerによりドライバーをインストール
	# chromiumを使用したいのでchrome_type引数でchromiumを指定しておく
	CHROMEDRIVER = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
	service = fs.Service(CHROMEDRIVER)
	driver = webdriver.Chrome(
							  options=options,
							  service=service
							 )


	# # webページ上のタイトル画像を取得
	# img = driver.find_element(By.TAG_NAME, 'img')
	# src = img.get_attribute('src')

	# # 取得した画像をカレントディレクトリに保存
	# with open(f"tmp_img.png", "wb") as f:
	# 	f.write(img.screenshot_as_png)

	# # 保存した画像をstreamlitアプリ上に表示
	# st.image("tmp_img.png")

##################################################################################

	# **********************************************************************
	# Instagram パラメータ
	# **********************************************************************
	# Instagram_Id='feelworld999'
	# Instagram_Password='19920619'
	# Follower_List_Url='https://www.instagram.com/hina_k_1019/followers/?hl=ja'
	# Loop_Count=4

	Follower_List_Url= 'https://www.instagram.com/' + Follower_List_Id + '/?hl=ja'
	Url='https://www.instagram.com/accounts/login/'

	# Time_S=590
	# Time_E=600
	Time_S=5
	Time_E=6
	
	Wait_Time=5

	# **********************************************************************
	# プログレスバー
	# **********************************************************************
	progress_text = "処理中です."
	percent_complete = 0
	my_bar = st.progress(percent_complete, text=progress_text)
	
	# **********************************************************************
	# インスタグラム　ログイン
	# **********************************************************************
	# Follow_Count=number
	try:
		driver.get(Url)

		# 停止
		time.sleep(Wait_Time)

		# ログインフォームの要素取得
		loginForm = driver.find_element(By.ID,"loginForm")

		# ユーザー名入力
		loginForm.find_element(By.NAME,"username").send_keys(Instagram_Id)

		# パスワード
		loginForm.find_element(By.NAME,"password").send_keys(Instagram_Password)
		
		# 一時停止
		time.sleep(Wait_Time)

		# Instagram Loginボタンクリック
		btns = driver.find_elements(By.TAG_NAME,"button")
		for i in btns:
			if i.text == 'Log In' or i.text == 'Log in':
				i.click()
				break

		time.sleep(Wait_Time)


		# **********************************************************************
		# プログレスバー
		# **********************************************************************
		percent_complete = 10
		my_bar.progress(percent_complete)

		# 停止
		time.sleep(Wait_Time)

		# **********************************************************************
		# フォロワー一覧を取得
		# **********************************************************************
		# パラメータでセットシタフォロワー一覧画面を表示
		driver.get(Follower_List_Url)

		# 停止
		time.sleep(Wait_Time)

		for j in range(1,Loop_Count):
			# **********************************************************************
			# プログレスバー
			# **********************************************************************
			
			percent_complete = ( j / Loop_Count ) 
			my_bar.progress(percent_complete)

			# ランダム整数を生成し、待機時間とする
			time.sleep(random.randint(Time_S, Time_E))
			st.write("写真撮影前")
			# スクリーンショットを取得
			Pict_Name= 'screenshot_' + str(j) + '.png'
			driver.save_screenshot(Pict_Name)

			# 保存した画像をstreamlitアプリ上に表示
			st.image(Pict_Name)
			st.write("写真撮影OK")
			k=j
			while True:
			# フォローボタンのXpathのセット
				Follow_Xpath = '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[' + str(k) + ']/div/div/div/div[3]/div/button'
				print(Follow_Xpath)
				button=driver.find_element(By.XPATH, Follow_Xpath)

				# フォロー済みかどうか,かつ処理回数が偶数かどうかで分岐
				if  button.text  ==  'フォローする' and k % 2 == 0:
					button.click()
					print(button.text)
					break
				else:
					# フォロー済みの場合はカウント上限を加算する
					print('クリックしない')
				k = k + 1


	except EWxception:
		# スクリーンショットを取得
		Pict_Name= 'screenshot_error.png'
		driver.save_screenshot(Pict_Name)

		# 保存した画像をstreamlitアプリ上に表示
		st.image(Pict_Name)

		# 処理終了メッセージ
		st.write("処理が途中で完了しました。")
		my_bar.empty()

		# webページを閉じる
		driver.close()

#####################################################################################


	# webページを閉じる
	driver.close()

	# スクレピン完了したことをstreamlitアプリ上に表示する
	st.write("正常終了。" + str(j) + "件をフォローしました。")
	my_bar.empty()