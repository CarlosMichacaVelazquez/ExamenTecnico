import json

from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine, text
from tkinter.filedialog import askopenfilename
import pandas as pd

app = Flask(__name__)
engine = create_engine('postgresql+psycopg2://postgres:123456@localhost:5432/my_database')


@app.route('/')
def upload_excel():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        filename = request.files['file']
        with pd.ExcelFile(filename) as xls:
            df = pd.read_excel(xls)
            if df.columns.values[0] == 'Nombre':
                df.to_sql(name='empleados', con=engine, if_exists='append', index=False)
            elif df.columns.values[0] == 'Ciudad':
                df.to_sql(name='lugares', con=engine, if_exists='append', index=False)

    return 'Archivo cargado con éxito en la base de datos.'


@app.route('/table/<name>/<format>', methods=['GET'])
def get_table(name, format):
    with engine.connect() as connection:
        if format.upper() == 'A':
            result = connection.execute(text('SELECT * FROM'+' '+name))
            var = ({name: [dict(row) for row in result]})
            return jsonify(var)
        elif format.upper() == 'B':
            result = connection.execute(text('SELECT * FROM'+' '+name))
            var = ({name: [dict(row) for row in result]})
            to_json = jsonify(var)
            return to_json


if __name__ == "__main__":
    app.run()