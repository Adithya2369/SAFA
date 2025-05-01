from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Sample DataFrame
    actual_rating_flag = False
    actual_rating = 3.75
    positive = 15
    negative = 5
    neutral = 10
    ai_rating = 82
    data = {
        'Index': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        'Summarised Review': [
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
        ],
        'Rating': [1,2,3,4,5,6,7,8,9,10],
        'Sentiment': ['pos', 'pos', 'neg', 'neg', 'neu', 'neu', 'pos', 'pos', 'neg', 'neg',],
        'Tags': ['product', 'quality', 'cc', 'delivery', 'package', 'warehouse', 'quality', 'cc', 'delivery', 'package']
    }

    df = pd.DataFrame(data)

    # Render the HTML with the DataFrame
    return render_template('test.html', table=df.to_html(classes='table table-bordered', index=False), flg = actual_rating_flag, actr = actual_rating, pos = positive, neg = negative, neu = neutral, air = ai_rating)

if __name__ == '__main__':
    app.run(debug=True)
