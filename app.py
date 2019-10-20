from flask import Flask, request, render_template
import directions
app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
@app.route('/main', methods=["GET", "POST"])
def main_page():
    return render_template('index.html')

@app.route('/suggestions', methods=["GET", "POST"])
def suggest_parking():
    if request.method == 'POST':
        coordinates = request.form['field']
    return coordinates

if __name__ == '__main__':
	app.run(debug = True)