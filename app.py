from flask import Flask, request, redirect, jsonify, render_template
import os
import pandas as pd
import markdown
from werkzeug.utils import secure_filename
from app_functions import *

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


material = {}
def process_excel():
    global material  # Declare the global variable inside the function
    df = pd.read_excel('uploads/TestData.xlsx')
    # Extract the 'Text' column and convert it to a dictionary
    text_column = df['Text']
    material = text_column.to_dict()  # Assign to the global variable
    return material


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        message = "No selected file"
        #return "No selected file"
    if file:
        filename = secure_filename(file.filename)
        new_filename = 'stored_excel_file.xlsx'  # Custom name for future use
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
        message = "File uploaded successfully"
        process_excel()
    return render_template('upload.html', message=message)


@app.route('/summarize')
def summarize():
    return render_template('summarize.html')


@app.route('/analysis')
def analysis():
    result = perform_analysis(material)
    # Convert markdown to HTML
    result = markdown.markdown(result)
    return render_template('analysis.html', message=result)

@app.route('/suggest')
def suggest():
    result = suggested_improvements(material)
    # Convert markdown to HTML with ordered list numbering disabled
    html_content = markdown.markdown(result, extensions=['nl2br'], output_format='html5')
    return render_template('suggest.html', message=html_content)

@app.route('/safa')
def safa():
    return render_template('safa.html')

#####################################################
#trials of errors
@app.route('/404_copy')
def copy_404():
    return render_template('404.html')

@app.route('/500_copy')
def copy_500():
    return render_template('500.html')

@app.route('/502_copy')
def copy_502():
    return render_template('502.html')

@app.route('/503_copy')
def copy_503():
    return render_template('503.html')

##################################################
# ERROR HANDLERS
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(502)
def bad_request(e):
    return render_template('400.html'), 400

@app.errorhandler(503)
def unauthorized(e):
    return render_template('503.html'), 401

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)