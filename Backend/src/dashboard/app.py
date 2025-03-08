from flask import Flask, redirect, url_for, request
app = Flask(__name__)


@app.route('/', methods=['GET',])
def success():
    return "HELLO WORLD"


if __name__ == '__main__':
    app.run(debug=True)
  