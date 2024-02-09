from time import sleep
import streamlit as st
from selenium import webdriver
# from selenium.webdriver import ChromeOptions, Chrome
from useragent_changer import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome import service as fs
from selenium.webdriver import ChromeOptions
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.common.by import By


# ボタンを作成(このボタンをアプリ上で押すと"if press_button:"より下の部分が実行される)
press_button = st.button("自動フォロー開始")

# **********************************************************************
# 関数処理
# **********************************************************************
def get_concat_image(img1, img2, direction='v'):
	"""
	Image を縦方向か横方向に結合する

	Parameters
	---
	img1 : PIL.Image
		結合対象イメージ 1
	img2 : PIL.Image
		結合対象イメージ 2
	direction : str, default v
		結合方向。 v-> 縦方向, h -> 横方向
	"""	  

	from PIL import Image
	if direction == 'v':
		new_img = Image.new('RGB', (max(img1.width, img2.width), (img1.height + img2.height)))
		new_img.paste(img1, (0, 0))
		new_img.paste(img2, ((img1.width - img2.width) //  2, img1.height))
	elif direction == 'h':
		new_img = Image.new('RGB', ((img1.width + img2.width), max(img1.height, img2.height)))
		new_img.paste(img1, (0, 0))
		new_img.paste(img2, (img1.width, (img1.height - img2.height) // 2))
	else:
		return None

	return new_img

def get_screenshot_image(driver):
	"""
	スクリーンショットを取得し、スクロールバーを削除する。

	Parameters
	---
	driver : selenium.webdriver
	"""

	from PIL import Image
	import io

	c_width, c_height, i_width, i_height = driver.execute_script(
		'return [document.documentElement.clientWidth, document.documentElement.clientHeight, window.innerWidth, window.innerHeight]')

	image = Image.open(io.BytesIO(driver.get_screenshot_as_png()))

	w = image.size[0] * c_width	 // i_width	 
	h = image.size[1] * c_height // i_height

	return image.crop((0,0,w, h))


def get_full_screenshot_image(driver, wait_time=1.5):
	"""
	画面をスクロールしながら全画面を取得する

	Parameters
	---
	driver : selenium.webdriver
	wait_time: int, default 1.5
		一度ウェブページの末尾まで行ったあとに停止する時間。
		ウェブページの読み込み待ち時間の設定。
	"""

	import time
	## ページ読み込み
	s_height, c_height = driver.execute_script(
		'return [document.body.scrollHeight, document.documentElement.clientHeight]')
	driver.execute_script('window.scrollTo(0, arguments[0]);', s_height)
	time.sleep(wait_time)

	## 1 ページ目を入れる
	driver.execute_script('window.scrollTo(0, arguments[0]);', 0)
	full_page = get_screenshot_image(driver)

	## 少しずつスクロールしながらスクリーンショットを取得する
	for y_coord in range(c_height, s_height, c_height):
		driver.execute_script('window.scrollTo(0, arguments[0]);', y_coord)
		single_page = get_screenshot_image(driver)

		## 最後のスクロールは適度にクロップする
		if s_height - y_coord < c_height:
			h = single_page.size[1] * (c_height - (s_height - y_coord)) // c_height
			single_page = single_page.crop((0, h, single_page.size[0], single_page.size[1]))

		## スクリーンショットを結合する
		full_page = get_concat_image(full_page, single_page)

	## ページトップヘ戻る
	driver.execute_script('window.scrollTo(0, arguments[0]);', 0)

	return full_page


# **********************************************************************
# ボタン処理
# **********************************************************************


if press_button:
	# プラットフォームを設定（'Firefox'を設定）
	PLATFORM= 'iphone'

	# Webサイト「IPアドレス確認・環境情報取得ツール」にアクセス
	URL = 'https://develop.tools/env-variable/'

	# インスタンスを生成
	ua = UserAgent(PLATFORM)

	# ドライバのオプション
	options = ChromeOptions()

	# option設定を追加（設定する理由はメモリの削減）
	options.add_argument("--headless")
	options.add_argument('--disable-gpu')
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')

	# オプションを設定
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--user-agent=' + ua.set())

	# webdriver_managerによりドライバーをインストール
	# chromiumを使用したいのでchrome_type引数でchromiumを指定しておく
	CHROMEDRIVER = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
	service = fs.Service(CHROMEDRIVER)
	driver = webdriver.Chrome(
								options=options,
								service=service
								)

	# chromedriverを使用しブラウザを起動
	driver.get(URL)

	# 設定した秒数を待機後ブラウザを終了
	SECONDS = 5
	sleep(SECONDS)

	# スクリーンショットを取得
	# driver.save_screenshot('screenshot.png')
	## ブラウザの横幅･縦幅は実行前に自分で調整してください
	# driver.set_window_size(xxx, yyy)
	screenshot = get_full_screenshot_image(driver)
	screenshot.save('screenshot.png')
	
	# 保存した画像をstreamlitアプリ上に表示
	st.image('screenshot.png')

	driver.quit()