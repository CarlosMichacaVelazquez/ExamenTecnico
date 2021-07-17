import json

from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine, text
import pandas as pd

app = Flask(__name__)
engine = create_engine('postgresql+psycopg2://postgres:123456@localhost:5432/my_database')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload')
def upload_excel():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        filename = request.files['file']
        with pd.ExcelFile(filename) as xls:
            sheetName = str(xls.sheet_names)[2:-2]
            html = pd.read_excel(xls).to_html()
            df = pd.read_excel(xls)
            df.to_sql(sheetName, if_exists='replace', con=engine)

    return render_template('uploader.html', html_code=html)


@app.route('/table', methods=['GET', 'POST'])
def get_table():
    if request.method == 'POST':
        table_list = request.values['table_list']
        format_json = request.values['formato']
        with engine.connect() as connection:
            if format_json == 'A':
                result = connection.execute(f'SELECT * FROM "{table_list}"')
                json_format_a = jsonify({table_list: [dict(row) for row in result]})
                return json_format_a
            elif format_json == 'B':
                result = connection.execute(f"SELECT column_name FROM information_schema.columns WHERE table_schema = "
                                            f"'public' AND table_name = '{table_list}'")
                contex = {
                    'result': result,
                    'table_list': table_list
                }
                return render_template('optionC.html', **contex)
            elif format_json == 'C':
                empleados = "'empleado'"
                nombre = "'nombre'"
                consulta = (f'SELECT json_build_object({nombre},"Compania",'
                            f'{empleados},(select json_agg(row_to_json((select r from( select "Nombre","Email",'
                            f'"Fecha de ingreso") '
                            'r))))) as empresa FROM empleados GROUP by "Compania"')
                result = connection.execute(text(consulta))
                var = ([dict(row) for row in result])
                return jsonify(var)


@app.route('/table_b', methods=['GET', 'POST'])
def get_table_b():
    if request.method == 'POST':
        consult_b = request.values['consulta']
        table_name = request.values['table_name']
        with engine.connect() as conn:
            print(consult_b)
            result = conn.execute(f'SELECT {consult_b} FROM "{table_name}"')
            json_format_b = jsonify({table_name: [dict(row) for row in result]})
        return json_format_b


@app.route('/consult_table', methods=['GET'])
def consult_table():
    with engine.connect() as conn:
        result = conn.execute("SELECT table_name as nombre from information_schema.tables WHERE "
                              "table_schema='public' AND "
                              "table_type='BASE TABLE'")
        table_list = []
        for row in result:
            table_list.append(row['nombre'])
        return render_template('Consult.html', table_list=table_list)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
