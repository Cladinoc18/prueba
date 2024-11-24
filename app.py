from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurar la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definir el modelo de la base de datos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identificador único
    name = db.Column(db.String(80), nullable=False)  # Nombre del usuario
    email = db.Column(db.String(120), unique=True, nullable=False)  # Correo electrónico único

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('form.html')  # Renderizar el formulario

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']

    if name and email:
        # Crear un nuevo usuario y guardarlo en la base de datos
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        return f"Usuario {name} registrado con éxito."
    return "Por favor, completa todos los campos."

@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

if __name__ == '__main__':
    app.run(debug=True)