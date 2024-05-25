from flask import Flask, render_template, request, send_file
from hs.hardwear_scanner import run_script, run_mini
from cleaner import cleaner
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s', filename='app.log', filemode='a')
logger = logging.getLogger(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/hardwear_scanner')
def hardwear_scanner():
    cleaner()
    return render_template("hardwear_scanner.html")

@app.route('/hsminih')
def hsminih():
    cleaner()
    return render_template("hsminih.html")

@app.route('/process', methods=['POST'])
def process():
    if 'input_value' in request.form:
        remote_computer = request.form['input_value']
        processed_data = run_script(remote_computer)
        button = request.form['action']
        if button == 'download':
            file_path = f'{remote_computer}.txt'
            with open(file_path, 'w') as file:
                file.write(processed_data)
            return send_file(file_path, as_attachment=True)
        else:
            processed_data_blocks = processed_data.split('\n\n')
            return render_template('process.html', processed_data_blocks=processed_data_blocks)
    else:
        return "нечего не ввел." 
    
@app.route('/hsmini', methods=['POST'])
def hsmini():
    if 'input' in request.form:
        remote_computer = request.form['input']
        mini_processed_data = run_mini(remote_computer)
        button = request.form['action']
        if button == 'download':
            file_path = f'{remote_computer}.txt'
            with open(file_path, 'w') as file:
                file.write(processed_data)
            return send_file(file_path, as_attachment=True)
        else:
            mini_processed_data_blocks = mini_processed_data.split('\n\n')
            return render_template('hsmini.html', mini_processed_data_blocks=mini_processed_data_blocks)
    else:
        return "нечего не ввел." 

if __name__ == '__main__':
    app.run(host='10.30.139.161', port=80, debug=True)