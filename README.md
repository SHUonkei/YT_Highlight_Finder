# YT_Highlight_Finder
## file説明
- RequestProcessor/get_funnytime.py
    - 草、wといった盛り上がりのタイミングで現れる文字列を含むコメントのみを抽出
- RequestProcessor/plot_chatdata.py
    - get_funnttime.pyで取得したデータから、最も瞬間該当コメント数が多かったタイミングの一分前から再生が開始される動画URLを生成する
- yt_highlight_finder/master.py
    - データをデータベースのテーブルに挿入する
- yt_highlight_finder/Template/App_Folder_HTML/video-list.html
    - http://127.0.0.1:8000/hello/video-list で表示されるhtml

## 準備
- install
```
pip install pytchat
pip install Django
pip install django-filter
pip install gspread
pip install youtube-search-python
```

## サーバー起動
```
cd yt_highlight_finder
python manage.py runserver
```

## 使い方
- http://127.0.0.1:8000/hello/
  - このurlがメインページ
- http://127.0.0.1:8000/hello/video-list
  - このページに動画一覧が表示される。サムネイルをクリックすると、その動画の最も盛り上がった可能性の高いタイミングの少し前から再生が開始される。
- https://docs.google.com/spreadsheets/d/1QJzxviVL3Hln1yvIpjm0bRsmAU4O-GitAjOd9DZtGQM/edit#gid=0
  - このスプレッドシートに動画の情報が保存されている。
  - 動画追加のリクエストをフロントエンドから送ると、リクエスト一覧に、自動で書き込まれる。
- 動画を追加したい場合、リクエスト一覧のスプレッドシートから、urlを取得し、RequestProcessor/main.pyのに貼り付け、実行する。ターミナルに、盛り上がったタイミングがみれるurlが生成されるので、それをスプレッドシートに書き込み、csv形式でダウンロートする。これをdata.csvとする。yt_highlight_finder直下にdata.csvを配置する。ここで、yt_highlight_finder/master.pyを実行すると、動画が追加される。




## databaseのsetup(cloneした時点で済まされているので実行する必要はない)

```
cd yt_highlight_finder
python manage.py migrate
python manage.py makemigrations hello
python manage.py sqlmigrate hello 0001
python manage.py migrate
python master.py
```
