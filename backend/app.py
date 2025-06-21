from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        database=os.getenv('POSTGRES_DB', 'bmi'),
        user=os.getenv('POSTGRES_USER', 'bmiuser'),
        password=os.getenv('POSTGRES_PASSWORD', 'bmipass')
    )

@app.route('/imc', methods=['POST'])
def calcul_imc():
    data = request.get_json()
    poids = data['poids']
    taille = data['taille']
    imc = poids / (taille ** 2)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO patients (poids, taille, imc) VALUES (%s, %s, %s)",
                (poids, taille, imc))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'IMC': round(imc, 2)})

@app.route('/patients', methods=['GET'])
def list_patients():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT poids, taille, imc FROM patients")
    results = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{'poids': r[0], 'taille': r[1], 'imc': r[2]} for r in results])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
