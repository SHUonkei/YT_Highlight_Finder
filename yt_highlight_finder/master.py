import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yt_highlight_finder.settings")  # プロジェクト名に応じて変更
import django
django.setup()
from hello.models import Hello  # アプリ名に応じて変更
import csv
# 空のリストを作成
hello_list = []



with open('./data.csv',encoding='utf-8') as f:
    reader = csv.reader(f)
    id_num = 1000
    for row in reader:
        new_hello = Hello()
        new_hello.videoid = id_num
        id_num += 1
        new_hello.title = row[1]
        new_hello.author = row[0]
        new_hello.url = row[3]
        print(row[3])
        new_hello.video = row[4]        
        new_hello.tag = row[-1]
        print(row)
        hello_list.append(new_hello)

# bulk_createを使用して一括保存
Hello.objects.bulk_create(hello_list)
