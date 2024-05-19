from flask import Flask, render_template, request, send_file
#from hs import hardwear_scanner
from process_data import process_data


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/test')
def test():
    return render_template("test.html")

@app.route('/process', methods=['POST'])
def process():
    input_data = request.form['input_value']
    processed_data = process_data(input_data)
    button = request.form['action']
    
    if button == 'download':
        with open('processed_data.txt', 'w') as file:
            file.write(processed_data)
        return send_file('processed_data.txt', as_attachment=True)
    else:
        return processed_data
if __name__ == '__main__':
     app.run(debug=True)