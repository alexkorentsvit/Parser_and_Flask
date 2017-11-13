from flask import render_template, redirect, session, request
from app import app
import psycopg2





@app.route('/', methods = ['GET'])
@app.route('/Table_LE', methods = ['GET'])
def Table():
    data = []
    try:
        conn = psycopg2.connect("dbname='uo_db2' user='alex_korentsvit' host='localhost' password='qwerty'")
    except:
        print ("I am unable to connect to the database")
    else:
        print('successfully connected to the database')
        cur = conn.cursor()
        cur.execute("SELECT id, EDRPOU_code, Name, State FROM UO_TABLE")
        counter = 0
        for record in cur:
            data.append(record)
            counter += 1
            if counter == 500:
                break
                            
        return render_template('Table_LE.html',
                               title = 'Table',
                               data = data)
