from flask import Flask, request, redirect, jsonify, render_template
import os
import pandas as pd
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


# def perform_analysis():
#     return "Analysis completed: Data is well-structured and balanced."
#
# def suggested_improvements():
#     return "Suggested Improvements: Consider adding more training samples for better accuracy."


@app.route('/analysis')
def analysis():
    result = perform_analysis(material)
    return render_template('analysis.html', message=result)

@app.route('/suggest')
def suggest():
    result = suggested_improvements(material)
    return render_template('suggest.html', message=result)

if __name__ == '__main__':
    app.run(debug=True)