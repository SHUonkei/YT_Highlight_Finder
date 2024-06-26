import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yt_highlight_finder.settings")  # プロジェクト名に応じて変更
import django
django.setup()
from stream_snapper.models import StreamSnapper  # アプリ名に応じて変更
import csv

import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials 

#env
import os
from dotenv import load_dotenv

#api
import requests

import utils
from youtubesearchpython import *

from pathlib import Path

def processRequests():
    BASE_DIR = Path(__file__).resolve().parent
    ENV_FILE = BASE_DIR / '.env'
    APP_CONFIG_JSON = BASE_DIR / 'stream_snapper/config.json'

    # .envファイルの内容を読み込見込む
    load_dotenv(ENV_FILE)
    #load_dotenv('./.env')

    #スプシからリクエストを読み取り、apiをたたき、動画一覧に書き込む.

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    #credentials = ServiceAccountCredentials.from_json_keyfile_name('./app/stream_snapper/config.json', scope)
    credentials = ServiceAccountCredentials.from_json_keyfile_name(APP_CONFIG_JSON, scope)
    gc = gspread.authorize(credentials)

    SPREAD_SHEET_KEY= os.environ['API_KEY']
    #CSV_FILENAME = "./request.csv"
    SHEET_NAME='request'
    TARGET_SHEET_NAME='動画一覧'
    workbook = gc.open_by_key(SPREAD_SHEET_KEY)
    worksheet = workbook.worksheet(SHEET_NAME)

    data_list = []

    i = 0
    while True:
        i += 1
        #get url
        Val = worksheet.acell('C'+str(i)).value
        if Val == None: break
        data = {'url': Val}
        
        # 行iの1列目から10列目までを空にする
        for j in range(1,6):
            worksheet.update_cell(i, j, "")   
        #apiをたたく
        responsejson = utils.urlGetRequest(data)
        targetUrl = responsejson.get('funny_time_url', 'URLの取得に失敗しました')
        
        #スプシに登録
        ws = workbook.worksheet(TARGET_SHEET_NAME)
        last_row =len(ws.col_values(1))
        next_row = last_row + 1
        videoInfo = Video.getInfo(Val)
        items = [videoInfo["channel"]["name"],videoInfo["title"],Val,targetUrl,videoInfo["id"]]
        ws.append_row(items , table_range='A'+str(next_row))
        
        # SQLite の database に登録
        new_record = StreamSnapper()
        total_records = StreamSnapper.objects.count()
        new_record.videoid = total_records
        new_record.title = videoInfo["title"]
        new_record.author = videoInfo["channel"]["name"]
        new_record.url = targetUrl
        new_record.video = videoInfo["id"]        
        new_record.tag = ""
        data_list.append(new_record)

    StreamSnapper.objects.bulk_create(data_list)

processRequests()
