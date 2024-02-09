from selenium.webdriver import ChromeOptions, Chrome
from useragent_changer import UserAgent
from time import sleep

# プラットフォームを設定（'Firefox'を設定）
PLATFORM= 'iphone'

# Webサイト「IPアドレス確認・環境情報取得ツール」にアクセス
URL = 'https://develop.tools/env-variable/'

# インスタンスを生成
ua = UserAgent(PLATFORM)

# オプションを設定
options = ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--user-agent=' + ua.set())

# chromedriverを使用しブラウザを起動
driver = Chrome(options=options)
driver.get(URL)

# 設定した秒数を待機後ブラウザを終了
SECONDS = 5
sleep(SECONDS)
driver.quit()