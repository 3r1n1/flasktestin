from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workers1.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<Task %r>' % self.id

class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(30),nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    workers = db.relationship('Todo', backref="roles")
    def __repr__(self):
        return '<Role %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        roles_roles = request.form['role']
        new_task = Todo(content=task_content)
        new_role = Roles(role=roles_roles)

        try:
            db.session.add(new_task)
            db.session.add(new_role)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your worker'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        roles = Roles.query.order_by(Roles.date_created).all()
        return render_template('index.html', tasks=tasks, roles=roles)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    role_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.delete(role_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that worker'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    role = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        role.role = request.form['role']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your worker'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
