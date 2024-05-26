from flask import Flask, render_template, request, send_file, abort, redirect, url_for
from hs.hardwear_scanner import run_script, run_mini
from installer.ninja_installer import install_package
from cleaner import cleaner
import logging
import os
import json

my_ip ='192.168.1.224'
bug_reports = []

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s', filename='app.log', filemode='a', encoding="utf-8")
logger = logging.getLogger(__name__)

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'wait_list.json')
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
    wait_list = data.get('wait_list', [])
    
@app.before_request        
def limit_remote_addr():
    if request.remote_addr not in wait_list:
        ip_address = request.remote_addr
        logger.warning(f"лезет без доступа {ip_address}")
        abort(403,f'пришли мне свой ip в джабер выдам инвайт') 
        
@app.route('/')
def home():
    cleaner()
    return render_template('home.html')

@app.route('/installer')
def installer():
    cleaner()
    return render_template('installer.html')

@app.route('/install_process', methods=['POST'])
def install_process():   
    result_install = install_package(request.form.get('input_value'), request.form.get('selected_file_path'))
    return render_template('install_process.html', result_install=result_install)
   
@app.route('/faq', methods=['GET', 'POST'])
def faq():
    file_path = "bug_report.log"
    bug_description = request.form.get('bug_description')
    if bug_description:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f"{bug_description}\n")
    return render_template("faq.html")

@app.route('/hardwear_scanner')
def hardwear_scanner():
    cleaner()
    return render_template("hardwear_scanner.html")

@app.route('/warehouse')
def warehouse():
    cleaner()
    return render_template("warehouse.html")

def process_request(input_value, run_function, template_name):
    if input_value:
        try:
            remote_computer = input_value
            processed_data = run_function(remote_computer)
            button = request.form['action']
            
            if button == 'download':
                file_path = f'{remote_computer}.txt'
                with open(file_path, 'w') as file:
                    file.write(processed_data)
                return send_file(file_path, as_attachment=True)
            else:
                processed_data_blocks = processed_data.split('\n\n')
                return render_template(template_name, processed_data_blocks=processed_data_blocks)
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            abort(500, description="Internal Server Error")
    else:
        return "Не введено значение."

@app.route('/hs_results', methods=['POST'])
def hs_results():
    return process_request(request.form.get('input_value'), run_script, 'hs_results.html')

@app.route('/warehouse_results', methods=['POST'])
def warehouse_results():
    return process_request(request.form.get('input'), run_mini, 'hs_results.html')

if __name__ == '__main__':
    app.run(host=f'{my_ip}', port=80, debug=True)