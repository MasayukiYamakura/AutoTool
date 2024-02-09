from selenium.webdriver import ChromeOptions, Chrome
from useragent_changer import UserAgent
from time import sleep
import streamlit as st

# ボタンを作成(このボタンをアプリ上で押すと"if press_button:"より下の部分が実行される)
press_button = st.button("自動フォロー開始")



if press_button:
    # プラットフォームを設定（'Firefox'を設定）
    PLATFORM= 'iphone'

    # Webサイト「IPアドレス確認・環境情報取得ツール」にアクセス
    URL = 'https://develop.tools/env-variable/'

    # インスタンスを生成
    ua = UserAgent(PLATFORM)

    # option設定を追加（設定する理由はメモリの削減）
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # オプションを設定
    options = ChromeOptions()
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
    driver.quit()