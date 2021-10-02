## 環境
- python = 3.9.6


## Django_setup
pip install pipenv
cd < Move Directory >
pipenv shell
pipenv install django
pipenv install --dev flake8 autopep8
pipenv shell


## How to start projects
"config"フォルダを作成（ここで全体のセッティングなどを行う）
django-admin startproject config .
ローカルのIPアドレスをget -> サイトが立ち上がる
python manage.py runserver