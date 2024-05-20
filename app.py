from flask import Flask, render_template, request, send_file

from hs.hardwear_scanner import run_script


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
    remote_computer = request.form['input_value']
    processed_data = run_script(remote_computer)
    button = request.form['action']
    
    if button == 'download':
        with open('processed_data.txt', 'w') as file:
            file.write(processed_data)
        return send_file('processed_data.txt', as_attachment=True)
    else:
        return processed_data
if __name__ == '__main__':
     app.run(debug=True)