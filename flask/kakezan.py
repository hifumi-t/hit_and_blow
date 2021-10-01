from flask import *

# Flaskオブジェクトの生成
app = Flask(__name__)

# ルート( / )へアクセスがあった時 --- (*1)


@app.route("/")
def root():
    # HTMLでWebフォームを記述 --- (*2)
    return """
    <html><body>
    <form action="/calc" method="post">
      <input type="text" name="a"> ×
      <input type="text" name="b">
      <input type="submit" value="計算">
    </form>
    """

# フォームの値を受け取って結果を表示 --- (*3)


@app.route("/calc", methods=["post"])
def calc():
    a = int(request.form.get("a"))
    b = int(request.form.get("b"))
    r = a * b
    return "<h1>答えは..." + str(r) + "</h1>"


# サーバーを起動
if __name__ == "__main__":
    app.run(debug=True, port=8888)
