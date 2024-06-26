# Stream snapper 

## 説明

youtubeライブで盛り上がったシーンを自動抽出するアプリ. また, それらを共有するプラットフォームの開発も行った. 

## 紹介スライド

<https://docs.google.com/presentation/d/1-x-z-yi8CvRIRrpr-fjHsA1q0IKzUEhoZpdMp1ldboE/edit#slide=id.g2c56f4f11e4_0_11>

## 使い方

### 準備

最初に `.env` を用意する必要があります。
サンプルは、`sample.env` にあるので、そちらを参照して作成してください。

それから、次の手順で環境を用意します。

Python 仮想環境の用意と有効化

```console
python -m venv venv
. venv/bin/activate
```

google cloudのプロジェクトを作成してサービスアカウントを作成. 管理用スプシに対象アカウントを招待してください.また, sample.config.jsonを参照して, config.jsonを作成してください.

必要なパッケージのインストール

```console
pip install -r requirements.txt
```

データベースの初期化

```console
python app/manage.py migrate
```

初期データの投入。DB 初期化にあたって自分で初期データを用意する場合は `app/init_db.csv` を作成します。サンプルが `app/sample.init_db.csv` にあるので、そちらを参照して作成してください。なお、`app/init_db.csv` がない場合は `app/sample.init_db.csv` が使われます。

```console
python app/init_db.py
```

### 起動

api

```console
python RequestProcessor/api_main.py
```

django app

```console
python app/manage.py runserver
```
