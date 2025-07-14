from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM gastos ORDER BY fecha DESC')
    gastos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', gastos=gastos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        concepto = request.form['concepto']
        monto = request.form['monto']
        fecha = request.form['fecha']
        categoria = request.form['categoria']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO gastos (concepto, monto, fecha, categoria) VALUES (%s, %s, %s, %s)',
                    (concepto, monto, fecha, categoria))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('agregar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        concepto = request.form['concepto']
        monto = request.form['monto']
        fecha = request.form['fecha']
        categoria = request.form['categoria']
        cur.execute('UPDATE gastos SET concepto=%s, monto=%s, fecha=%s, categoria=%s WHERE id=%s',
                    (concepto, monto, fecha, categoria, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    else:
        cur.execute('SELECT * FROM gastos WHERE id = %s', (id,))
        gasto = cur.fetchone()
        cur.close()
        conn.close()
        return render_template('editar.html', gasto=gasto)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM gastos WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)