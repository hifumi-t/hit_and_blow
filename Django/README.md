## 環境
- python = 3.9.6


## Django setup
```sh
pip install pipenv
< Move Directory >
pipenv install --python 3.9.6
pipenv install requests django brython
pipenv install --dev flake8 autopep8
pipenv shell
```

## How to use
- ローカルIPアドレスをget -> [cmd]+クリック -> サイトが立ち上がる
```sh
python manage.py runserver
```
- 立ち上げた状態では ”NOT FOUND” -> URLの尻に以下を追加
- サインイン画面（Bootstrapテンプレ）
```sh
<"local IP address you got"　+ "/sign">
```
- 計算機
```sh
<"local IP address you got"　+ "/cal">
```
- BMI計算（Brythonが使えているかの確認）
```sh
<"local IP address you got"　+ "/bmi">
```

