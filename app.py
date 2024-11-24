import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurar PostgreSQL o usar SQLite como respaldo
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:///database.db'  # Usa SQLite si no hay variable de entorno
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de base de datos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    if name and email:
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        return f"Usuario {name} registrado con éxito."
    return "Por favor, completa todos los campos."

if __name__ == '__main__':
    app.run(debug=True)