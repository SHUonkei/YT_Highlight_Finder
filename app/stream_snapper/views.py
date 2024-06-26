#HttpResponseクラス:クライアントに送り返す内容を管理するクラス
from django.shortcuts import render
from django.http import HttpResponse
from . import forms
from django.views.generic import TemplateView
from .models import StreamSnapper
from youtubesearchpython import *


#スプシ周り
import gspread
from oauth2client.service_account import ServiceAccountCredentials
                
#api用
import requests

#env
import os
from dotenv import load_dotenv

import utils
def index(request):
    
    #変数使う場合はここで置き換えて表示
    #render の返り値: TemplateResponseクラスのインスタンス
    
    params = {
        'title':"this is title parameter",
        'msg':"this is a page for testing",
        'goto':'videoListView',
        'goToGenerateUrl':'GenerateUrl',
        'gotoform':'formpage',
        'analyzeUrl':'analyzeUrl',
    }
    
    return render(request, 'stream_snapper/index.html',params)

def videoListView(request):
    ctx = {
        'title':"this is title parameter",
        'msg':"this is a page for testing",
        'goto':'videoListView',
        'goToGenerateUrl':'GenerateUrl',
        'gotoform':'formpage',
        'analyzeUrl':'analyzeUrl',
    }
    template_name = "stream_snapper/video-list.html"
    
    query = request.GET.get('q', '')  # 'q' は検索ボックスの名前
    if query:
        qs = StreamSnapper.objects.filter(title__icontains=query)
    else:
        qs = StreamSnapper.objects.all()
    ctx["object_list"] = qs
    return render(request, template_name, ctx)

class generateUrlView(TemplateView):
    def __init__(self):
        self.params = {
            "Message":"情報を入力してください。",
            "form": forms.Contact_Form(),  # 'forms' ファイルからインスタンスを取得
            'goto':'videoListView',
            'goToGenerateUrl':'GenerateUrl',
            'gotoform':'formpage',
            'analyzeUrl':'analyzeUrl',
        }

    def get(self, request):
        return render(request, "stream_snapper/generateUrl.html", context=self.params)

    def post(self, request):
        self.params["form"] = forms.Contact_Form(request.POST)
        if self.params["form"].is_valid():
            self.params["Message"] = "リクエストを受け付けました！ありがとうございます！"
            url = request.POST['Website']
            data = {'url': url}
            responsejson = utils.urlGetRequest(data) 
            self.params["response"] = responsejson.get('funny_time_url', 'URLの取得に失敗しました')
        # エラーの場合でも同じテンプレートを使用
        return render(request, "stream_snapper/generateUrl.html", context=self.params)

class analyzeUrlView(TemplateView):
    def __init__(self):
        self.params = {
            "Message":"情報を入力してください。",
            "form": forms.Contact_Form(),  # 'forms' ファイルからインスタンスを取得
            'goto':'videoListView',
            'goToGenerateUrl':'GenerateUrl',
            'gotoform':'formpage',
            'analyzeUrl':'analyzeUrl',
        }

    def get(self, request):
        return render(request, "stream_snapper/analyzeUrl.html", context=self.params)

    def post(self, request):
        self.params["form"] = forms.Contact_Form(request.POST)
        if self.params["form"].is_valid():
            self.params["Message"] = "リクエストを受け付けました！ありがとうございます！"
            url = request.POST['Website']
            data = {'url': url}
            responsejson = utils.analyzeRequest(data) 
            self.params['image_base64'] = responsejson.get('image', 'URLの取得に失敗しました')
        # エラーの場合でも同じテンプレートを使用
        return render(request, "stream_snapper/analyzeUrl.html", context=self.params)

class FormView(TemplateView):
    # 初期変数定義
    def __init__(self):
        self.params = {"Message":"情報を入力してください。",
                       "form":forms.Contact_Form(),#forms ファイルから 'form'という値にインスタンスが設定される
                       'goto':'videoListView',
                       'goToGenerateUrl':'GenerateUrl',
                       'gotoform':'formpage',
                       'analyzeUrl':'analyzeUrl',
                       }

    # GET時の処理を記載
    def get(self,request):
        return render(request, "stream_snapper/formpage.html",context=self.params)

    # POST時の処理を記載
    def post(self,request):
        if request.method == "POST":
            self.params["form"] = forms.Contact_Form(request.POST)
            # フォーム入力が有効な場合
            if self.params["form"].is_valid():
                self.params["Message"] = "リクエストを受け付けました！ありがとうございます！"
                #urlが無効なとき（youtubeとかじゃないときの例外処理必要
                SERVICE_ACCOUNT_FILE = 'stream_snapper/config.json'
                #jsonファイルを使って認証情報を取得
                scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
                cretentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)

                #認証情報を使ってスプレッドシートの操作権を取得
                gs = gspread.authorize(cretentials)

                #スプレッドシートのキーを使ってシートの情報を取得
                SPREADSHEET_KEY = '1QJzxviVL3Hln1yvIpjm0bRsmAU4O-GitAjOd9DZtGQM'

                ws = gs.open_by_key(SPREADSHEET_KEY).worksheet('request')
                last_row =len(ws.col_values(1))
                next_row = last_row + 1

#               url:"https://www.youtube.com/watch?v=AZOr7GuxLPQ"
                url = request.POST['Website']
                videoInfo = Video.getInfo(url)

                items = [videoInfo["channel"]["name"],videoInfo["title"],url,"",videoInfo["id"]]
                ws.append_row(items , table_range='A'+str(next_row))


        return render(request, "stream_snapper/formpage.html",context=self.params)




"""
これより先は使用していないコード
今後の機能拡張に使えるかもしれない
"""

def next(request):
    params = {
        'title':"next"
        ,'msg':"this is next page"
        ,'goto':'index',
    }
    return render(request, 'stream_snapper/index.html',params)
