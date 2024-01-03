from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    # Read the CSV file
    df = pd.read_csv('experiment_log.csv')
    # no index column
    # df.to_csv('experiment_log.csv', index=False)
    # remove brackets from the entries
    df = df.replace({'\[': '', '\]': ''}, regex=True)
    # remove quotes from the entries
    df = df.replace({'\'': ''}, regex=True)
    # convrt the last column to a clickable link
    print(df['link'])
    df['link'] = df['link'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')

    # Convert the DataFrame to HTML
    table = df.to_html(escape=False)

    # Create a simple HTML template
    template = """
    <html>
        <head>
            <title>Job Manager</title>
            <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
        </style>
        </head>
        <body>
            <h1>Jobs</h1>
            {{ table|safe }}
        </body>
    </html>
    """

    # Render the template with the table
    return render_template_string(template, table=table)

if __name__ == '__main__':
    app.run(debug=True)