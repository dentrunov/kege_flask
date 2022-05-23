from flask import Flask, request, render_template

from flask_moment import Moment

app = Flask(__name__, static_folder="static")
moment = Moment(app)
print(type(moment))

@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/test/')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    #не забыть снять дебаг
    app.run(debug=True)
