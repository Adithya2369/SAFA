from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Sample DataFrame
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Hannah', 'Ian', 'Judy'],
        'ID': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        'Country': ['USA', 'UK', 'Canada', 'Australia', 'Germany', 'India', 'France', 'Japan', 'Brazil', 'South Africa'],
        'Sentence': [
            "Alice enjoys hiking on weekends.",
            "Bob is learning to play the guitar.",
            "Charlie works as a data analyst.",
            "David travels frequently for business.",
            "Eva speaks three languages fluently.",
            "Frank runs a local bakery.",
            "Grace volunteers at the animal shelter.",
            "Hannah is writing a science fiction novel.",
            "Ian loves mountain biking.",
            "Judy teaches mathematics at a university."
        ]
    }

    df = pd.DataFrame(data)

    # Render the HTML with the DataFrame
    return render_template('summarise.html', table=df.to_html(classes='table table-bordered', index=False))

if __name__ == '__main__':
    app.run(debug=True)
