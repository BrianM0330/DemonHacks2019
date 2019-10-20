from flask import Flask, request, render_template
import directions
app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
@app.route('/main', methods=["GET", "POST"])
def main_page():
    return render_template('index.html')

@app.route('/suggestions')
def suggest_parking():
    coordinates = request.form['search']
    return coordinates

if __name__ == '__main__':
	app.run(debug = True)