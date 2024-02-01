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

#############################################################
# 追加箇所
#############################################################
import dataclasses
import threading
import time


class Worker(threading.Thread):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# self.counter = 0
		self.should_stop = threading.Event()
		
	def run(self):
		while not self.should_stop.wait(0):
			time.sleep(1)
			# self.counter += 1
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

			# **********************************************************************
			# Instagram パラメータ
			# **********************************************************************
			Follower_List_Url= 'https://www.instagram.com/' + Follower_List_Id + '/followers/?hl=ja'
			Url='https://www.instagram.com/accounts/login/'

			Time_E = Time_S + 3
			Wait_Time=5

			# **********************************************************************
			# プログレスバー
			# **********************************************************************
			progress_text = "処理開始しました."
			percent_complete = 0
			my_bar = st.progress(percent_complete, text=progress_text)
			
			# **********************************************************************
			# インスタグラム　ログイン
			# **********************************************************************
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

				# **********************************************************************
				# プログレスバー
				# **********************************************************************
				progress_text = "ログインに成功しました."
				percent_complete = 5
				my_bar.progress(percent_complete, text=progress_text)


				time.sleep(Wait_Time)

				# スクリーンショットを取得
				driver.save_screenshot('screenshot.png')
				# 保存した画像をstreamlitアプリ上に表示
				st.image('screenshot.png')

				# **********************************************************************
				# フォロワー一覧を取得
				# **********************************************************************
				# パラメータでセットシタフォロワー一覧画面を表示
				driver.get(Follower_List_Url)

				time.sleep(Wait_Time)

				# スクリーンショットを取得
				driver.save_screenshot('screenshot.png')
				# 保存した画像をstreamlitアプリ上に表示
				st.image('screenshot.png')

				# **********************************************************************
				# プログレスバー
				# **********************************************************************
				progress_text = "フォロワー一覧画面に遷移しました."
				percent_complete = 10
				my_bar.progress(percent_complete, text=progress_text)


				# 停止
				time.sleep(Wait_Time)

				# **********************************************************************
				# プログレスバー
				# **********************************************************************
				progress_text = "フォロー処理を行っています."
				percent_complete = 15
				my_bar.progress(percent_complete, text=progress_text)

				# **********************************************************************
				# 繰り返し処理
				# **********************************************************************
				for j in range(1,Loop_Count):
					# ランダム整数を生成し、待機時間とする
					time.sleep(random.randint(Time_S, Time_E))
					
					# スクリーンショットを取得
					driver.save_screenshot('screenshot.png')
					# 保存した画像をstreamlitアプリ上に表示
					st.image('screenshot.png')
					
					# プログレスバー
					if	( j / Loop_Count ) * 100 <= 20:
						percent_complete = 20
					elif ( j / Loop_Count ) * 100 <= 30:
						percent_complete = 30
					elif ( j / Loop_Count ) * 100 <= 40:
						percent_complete = 40
					elif ( j / Loop_Count ) * 100 <= 50:
						percent_complete = 60
					elif ( j / Loop_Count ) * 100 <= 70:
						percent_complete = 70
					elif ( j / Loop_Count ) * 100 <= 80:
						percent_complete = 80
					elif ( j / Loop_Count ) * 100 <= 90:
						percent_complete = 90
					else:
						percent_complete = 98
					progress_text = str(j) + '/' + str(Loop_Count) + '件のフォローが完了しました.'
					my_bar.progress(percent_complete, text=progress_text)
					
					k=j
					while True:
						try:
							# フォローボタンのXpathのセット
							Follow_Xpath = '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[' + str(k) + ']/div/div/div/div[3]/div/button'

							button=driver.find_element(By.XPATH, Follow_Xpath)

							# 要素までスクロール
							driver.execute_script("arguments[0].scrollIntoView();", button)

							# フォロー済みかどうか,かつ処理回数が偶数かどうかで分岐
							if	button.text	 ==	 'フォローする' and k % 2 == 0:
								button.click()
								break
							else:
								# フォロー済みの場合はカウント上限を加算する
								print('クリックしない')
							k = k + 1
						except Exception:
							# 要素までスクロール
							driver.execute_script("arguments[0].scrollIntoView();", Follow_Xpath)

			# **********************************************************************
			# 例外処理
			# **********************************************************************
			except Exception:
				# スクリーンショットを取得
				driver.save_screenshot('screenshot.png')
				# 保存した画像をstreamlitアプリ上に表示
				st.image('screenshot.png')

				# 処理終了メッセージ
				st.write("処理が途中で完了しました。")
				# my_bar.empty()

				# webページを閉じる
				driver.close()

			# スクレイピングが完了したことをstreamlitアプリ上に表示する
			# st.write("正常終了。" + str(j) + "件をフォローしました。")
			# my_bar.empty()

			# **********************************************************************
			# プログレスバー
			# **********************************************************************
			progress_text = "正常終了。" + str(j) + "件をフォローしました。"
			percent_complete = 100
			my_bar.progress(percent_complete, text=progress_text)

			# webページを閉じる
			driver.close()


@st.experimental_singleton
@dataclasses.dataclass
class ThreadManager:
	worker = None
	
	def get_worker(self):
		return self.worker
	
	def is_running(self):
		return self.worker is not None and self.worker.is_alive()
	
	def start_worker(self):
		if self.worker is not None:
			self.stop_worker()
		self.worker = Worker(daemon=True)
		self.worker.start()
		return self.worker
	
	def stop_worker(self):
		self.worker.should_stop.set()
		self.worker.join()
		self.worker = None



#要素をクリックする直前の処理を定義
# class CustomListener(AbstractEventListener):
#	  def before_click(self, element, driver):
#		  # 要素までスクロールさせる
#		  driver.execute_script('arguments[0].scrollIntoView({behavior: "smooth", block: "center"});', element)





#############################################################
# 追加箇所
#############################################################

def main():
	thread_manager = ThreadManager()

	# タイトルを設定
	st.title("Instagram Auto Follow")

	Instagram_Id = st.text_input('Instagram ID', placeholder='Instagram ID', max_chars=20, help='電話番号かメールアドレスかID')

	Instagram_Password = st.text_input('Instagram Password', placeholder='Instagram Password', max_chars=20)

	Follower_List_Id =	st.text_input('Follower List Id', placeholder='Follower List Id', max_chars=20, help='例 hina_k_1019')

	Loop_Count = st.number_input('フォローする件数',0,200,0,step=5)

	Time_S = st.number_input('フォローする時間間隔(秒)',0,600,0,step=5)

	# ボタンを作成(このボタンをアプリ上で押すと"if press_button:"より下の部分が実行される)
	press_button = st.button("自動フォロー開始")


	with st.sidebar:
		if st.button('Start worker', disabled=thread_manager.is_running()):
			worker = thread_manager.start_worker()
			st.experimental_rerun()
			
		if st.button('Stop worker', disabled=not thread_manager.is_running()):
			thread_manager.stop_worker()
			st.experimental_rerun()
	
	if not thread_manager.is_running():
		st.markdown('No worker running.')
	else:
		worker = thread_manager.get_worker()
		st.markdown(f'worker: {worker.getName()}')
		placeholder = st.empty()
		while worker.is_alive():
			placeholder.markdown(f'counter: {worker.counter}')
			time.sleep(1)

	# 別セッションでの更新に追従するために、定期的にrerunする
	time.sleep(1)
	st.experimental_rerun()

if __name__ == '__main__':
	main()
