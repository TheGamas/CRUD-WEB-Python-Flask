from flask import Flask, render_template, request, redirect, url_for
import os
import DBconection as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)

@app.route('/')
def home():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM RUTA_DE_REPARTO")

    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for row in myresult:
        insertObject.append(dict(zip(columnNames, row)))
    cursor.close()
    return render_template('index.html', data=insertObject)

@app.route('/add', methods=['POST'])
def add():
    numero_de_ruta = request.form['NUMERO_DE_RUTA']
    paquetes_entregados = request.form['PAQUETES_ENTREGADOS']
    incidencia = request.form['INCIDENCIA']

    cursor = db.cursor()
    cursor.execute("SELECT NUMERO_DE_RUTA FROM RUTA_DE_REPARTO")
    all_keys = [row[0] for row in cursor.fetchall()]

    if numero_de_ruta in all_keys:
        return redirect(url_for('home'))
    
    if paquetes_entregados and incidencia:
        cursor.execute("INSERT INTO RUTA_DE_REPARTO (NUMERO_DE_RUTA, PAQUETES_ENTREGADOS, INCIDENCIA)" 
                    + "VALUES (?, ?, ?)", (numero_de_ruta, paquetes_entregados, incidencia))
    
    elif paquetes_entregados and not incidencia:
        cursor.execute("INSERT INTO RUTA_DE_REPARTO (NUMERO_DE_RUTA, PAQUETES_ENTREGADOS)" 
                    + "VALUES (?, ?)", (numero_de_ruta, paquetes_entregados,))
    elif incidencia and not paquetes_entregados:
        cursor = db.cursor()
        cursor.execute("INSERT INTO RUTA_DE_REPARTO (NUMERO_DE_RUTA, INCIDENCIA)" 
                    + "VALUES (?, ?)", (numero_de_ruta, incidencia))
    else:
        cursor.execute("INSERT INTO RUTA_DE_REPARTO (NUMERO_DE_RUTA)" 
                    + "VALUES (?)", (numero_de_ruta,))
        
    db.commit()
    return redirect(url_for('home'))

@app.route('/delete/<string:id>', methods=['POST'])
def delete(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM RUTA_DE_REPARTO WHERE NUMERO_DE_RUTA = ?", (id,))
    db.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    paquetes_entregados = request.form['PAQUETES_ENTREGADOS']
    incidencia = request.form['INCIDENCIA']

    if paquetes_entregados and incidencia:
        cursor = db.cursor()
        cursor.execute("UPDATE RUTA_DE_REPARTO SET PAQUETES_ENTREGADOS = ?, INCIDENCIA = ? WHERE NUMERO_DE_RUTA = ?", (paquetes_entregados, incidencia, id))
        db.commit()
    elif paquetes_entregados and not incidencia:
        cursor = db.cursor()
        cursor.execute("UPDATE RUTA_DE_REPARTO SET PAQUETES_ENTREGADOS = ? WHERE NUMERO_DE_RUTA = ?", (paquetes_entregados, id))
        db.commit()
    elif incidencia and not paquetes_entregados:
        cursor = db.cursor()
        cursor.execute("UPDATE RUTA_DE_REPARTO SET INCIDENCIA = ? WHERE NUMERO_DE_RUTA = ?", (incidencia, id))
        db.commit()
    else:
        pass
    
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=16006)