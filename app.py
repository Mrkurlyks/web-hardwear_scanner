from flask import Flask, render_template, request, send_file, abort, redirect, url_for
from hs.hardwear_scanner import run_script, run_mini
from cleaner import cleaner
import logging

bug_reports = []

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s', filename='app.log', filemode='a')
logger = logging.getLogger(__name__)

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
    remote_computer = request.form.get('input_value')
    file_path = request.form.get('selected_file_path')
    return render_template('install_process.html', computer_name_or_ip=remote_computer, selected_file_path=file_path)
      
@app.route('/faq', methods=['GET', 'POST'])
def faq():
    cleaner()
    if request.method == 'POST':
        bug_description = request.form.get('bug_description')
        if bug_description:
            bug_reports.append(bug_description)
            return redirect(url_for('faq')) 
        return "Please provide a bug description."
    return render_template('faq.html')

@app.route('/admin_panel')
def admin_panel():
    enumerated_bug_reports = list(enumerate(bug_reports)) 
    file_path = "bug report.log"
    with open(file_path, 'w') as file:
        file.write(enumerated_bug_reports)
    return render_template('admin_panel.html', bug_reports=enumerated_bug_reports)

@app.route('/respond_to_bug', methods=['POST'])
def respond_to_bug():
    bug_report_id = int(request.form.get('bug_report_id'))
    admin_response = request.form.get('admin_response')
    if bug_report_id < len(bug_reports) and admin_response:
        bug_reports[bug_report_id] += f"\nОтвет: {admin_response}"
        return redirect(url_for('admin_panel'))
    return "Ошибочка."

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
    app.run(host='192.168.0.117', port=80, debug=True)