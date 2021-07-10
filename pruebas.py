import pandas as pd
from sqlalchemy import create_engine
from tkinter.filedialog import askopenfilename

''' Conexion a la base de datos '''
engine = create_engine('postgresql+psycopg2://postgres:123456@localhost:5432/my_database')


filename = askopenfilename()


with pd.ExcelFile(filename) as xls:
    df = pd.read_excel(xls)
    print(df)
    # if df.columns.values[0] == 'Nombre':
    #     df.to_sql(name='empleados', con=engine, if_exists='append', index=False)
    # elif df.columns.values[0] == 'Ciudad':
    #     df.to_sql(name='lugares', con=engine, if_exists='append', index=False)