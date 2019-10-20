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
    #pass the coordinates to a function that makes a query to the Google Maps API
    #pip install requirements
    #in terminal flask run
    #any errors..google them
    #@app.route is just directing to URLs
    #'/suggestions' leads to / and the suggestions endpoint
    return coordinates

if __name__ == '__main__':
	app.run(debug = True)