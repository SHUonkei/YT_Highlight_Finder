from django.shortcuts import render

#HttpResponseというクラスをimport
#クライアントに送り返す内容を管理するクラス

from django.http import HttpResponse
from . import forms
from django.views.generic import TemplateView
from . import get_funnytime
from . import plot_chatdata
from .models import Hello
from youtubesearchpython import *


def index(request):
    
    #render でレンダリングしてる
    #変数とかなんか使う場合はここで置き換えて表示させる
    #render の返り値は TemplateResponseというクラスのインスタンス
    
    params = {
        'title':"this is title parameter",
        'msg':"this is a page for testing",
        'goto':'videoListView',
        'gotoform':'formpage'
    }
    
    return render(request, 'hello/index.html',params)

def videoListView(request):
    template_name = "hello/video-list.html"
    ctx = {}
    
    query = request.GET.get('q', '')  # 'q' は検索ボックスの名前です
    if query:
        qs = Hello.objects.filter(title__icontains=query)
    else:
        qs = Hello.objects.all()
    ctx["object_list"] = qs
    return render(request, template_name, ctx)

class FormView(TemplateView):
    # 初期変数定義
    def __init__(self):
        self.params = {"Message":"情報を入力してください。",
                       "form":forms.Contact_Form(),#forms ファイルから 'form'という値にインスタンスが設定される
                       }

    # GET時の処理を記載
    def get(self,request):
        return render(request, "hello/formpage.html",context=self.params)

    # POST時の処理を記載
    def post(self,request):
        if request.method == "POST":
            self.params["form"] = forms.Contact_Form(request.POST)
            
            
            
            # フォーム入力が有効な場合
            if self.params["form"].is_valid():
                self.params["Message"] = "リクエストを受け付けました！ありがとうございます！"
                #urlが無効なとき（youtubeとかじゃないときの例外処理必要
                import gspread
                from oauth2client.service_account import ServiceAccountCredentials
                SERVICE_ACCOUNT_FILE = 'hello/config.json'
                #jsonファイルを使って認証情報を取得
                scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
                cretentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)

                #認証情報を使ってスプレッドシートの操作権を取得
                gs = gspread.authorize(cretentials)

                #共有したスプレッドシートのキー（後述）を使ってシートの情報を取得
                SPREADSHEET_KEY = '1QJzxviVL3Hln1yvIpjm0bRsmAU4O-GitAjOd9DZtGQM'
                ws = gs.open_by_key(SPREADSHEET_KEY).worksheet('動画一覧')
                #print(worksheet.acell("A2").value)
                last_row =len(ws.col_values(1))
                next_row = last_row + 1
#                url = "https://www.youtube.com/watch?v=AZOr7GuxLPQ"
                url = request.POST['Website']
                videoInfo = Video.getInfo(url)

                items = [videoInfo["channel"]["name"],videoInfo["title"],url,"",videoInfo["id"]]
                ws.append_row(items , table_range='A'+str(next_row))

                ws = gs.open_by_key(SPREADSHEET_KEY).worksheet('リクエスト一覧')
                #print(worksheet.acell("A2").value)
                last_row =len(ws.col_values(1))
                next_row = last_row + 1
#                url = "https://www.youtube.com/watch?v=AZOr7GuxLPQ"
                url = request.POST['Website']
                videoInfo = Video.getInfo(url)

                items = [videoInfo["channel"]["name"],videoInfo["title"],url,"",videoInfo["id"]]
                ws.append_row(items , table_range='A'+str(next_row))


        return render(request, "hello/formpage.html",context=self.params)



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
    return render(request, 'hello/index.html',params)



#ビュー関数
#クライアントからのHTTPリクエストを受け取り、
#それに対するHTTPレスポンスを返す役割
#ここでのrequestは、クライアントからのリクエスト情報を保持するオブジェクト

#リクエストが来たらする処理をかく
#requestはHttpRequestクラスのインスタンス
#クライアントからサーバーにアクセスする際の様々な情報をまとめて管理している
#対になる概念がHttpResponse
#もちろんクエリパラメータもその中に入っているので、dict形式で取得できる GETが辞書

# def index(request,id,nickname):
    #クエリパラメータをつかう　?id=1&name= みたいなところ 
    # if 'msg' in request.GET:
    #     msg = request.GET['msg']
    #     result = HttpResponse('You Typed: "'+msg+'".')
    # else:
    #     result = "please send msg parameter!"
    # return HttpResponse(result)
    
    # result = 'your id:' + str(id) + ', name: "' + nickname + '".'
    # return HttpResponse(result)
    
