import os
from flask import Flask, request, render_template
# import directions
app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
@app.route('/main', methods=["GET", "POST"])
def main_page():
    return render_template('index.html')

@app.route('/suggestions', methods=["GET", "POST"])
def suggest_parking():
    if request.method == 'POST':
        print(request.form)    
        coordinate = request.form['Submit']
        coordinate = coordinate.split(',')
        camera = coordinate[0]
        location = coordinate[1]
        print("Camera:", camera)
        print("Location:", location)
        os.system("python3 web_demo.py --CAM_ID=" + camera + " --location=" + location + " -pause=0.01 -w_patch=25 -h_patch=25 --method=0 --output=output.csv")
    #pass the coordinates to a function that makes a query to the Google Maps API
    #pip install requirements
    #in terminal flask run
    #any errors..google them
    #@app.route is just directing to URLs
    #'/suggestions' leads to / and the suggestions endpoint
    return location

if __name__ == '__main__':
	app.run(debug = True)