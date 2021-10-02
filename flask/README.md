# Flask使い方メモ
##### 作成者：tanaka，2021年10月2日

## Flaskアプリケーションの実行
- ディレクトリを移動
- FLASK_APP環境変数を設定しておく
- Powershellで以下を実行
```sh
> cd flask
> $env:FLASK_APP = "hello" # hello.pyがメインファイルの場合
> flask run
 * Running on http://127.0.0.1:5000/
```

## Debug Modeにする
- いちいちURLを生成して読み込む必要がなくなるのでオススメ
- Powershellで以下を実行
```sh
> $env:FLASK_ENV = "development"
> flask run
```

## 注意点
- Flaskはディレクトリ構造がカッチリ決まっている
- この構造じゃないとエラーが出る（出た）
- templatesの中にHTMLファイル，staticの中にCSSファイルを入れていく
```sh
top-tweets
├── app.py #Flaskの実行ファイル
└── templates
    └── index.html
└── static
    └── style.css
```

## 参考サイト
- YouTube動画
    - [たった50分でFlaskの基礎を習得！PythonによるWebアプリ開発 ~Flask超入門 vol.1~](https://www.youtube.com/watch?v=bzbrpkbjWe8)
    - [Flaskで簡易ブログアプリの作成！データベース操作も~Flask超入門 vol.2~](https://www.youtube.com/watch?v=mW0_60SRr3s)
    - [Flaskでサインアップ・ログイン機能の実装 ~Flask超入門 vol.3~](https://www.youtube.com/watch?v=Gyy1tzwenc8&t=2457s)
- Web記事
    - [Flask公式ドキュメント](https://flask.palletsprojects.com/en/2.0.x/)
        - [Quickstart](https://flask.palletsprojects.com/en/2.0.x/quickstart/#static-files)
        - [Tutorial](https://flask.palletsprojects.com/en/2.0.x/tutorial/)
        - [Template Designer Documentation](https://jinja.palletsprojects.com/en/3.0.x/templates/)
    - [Flaskの簡単な使い方 - Qiita](https://qiita.com/zaburo/items/5091041a5afb2a7dffc8)
    - [Pythonで最も使われているWebフレームワーク『Flask』を10分で学ぼう](https://news.mynavi.jp/article/zeropython-64/)
    - [FlaskvsDjango！PythonのWebアプリケーションフレームワークを徹底比較！](https://toukei-lab.com/flask-django)
    - [PythonのFlaskで簡単なWebアプリケーションを作ってみよう！](https://toukei-lab.com/python-flask)
    - [herokuを使ってPythonのflaskで作ったアプリケーションをデプロイする方法と注意点！](https://toukei-lab.com/heroku-python)