from logging import debug
from math import sqrt
from flask import Flask,render_template,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200),nullable=True)
    completed = db.Column(db.Integer,default=0)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST','GET'])
def index():
    if request.method== 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            return 'There was a issue'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "error in deletion"

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    if request.method == 'POST':
        task = Todo.query.get_or_404(id)
        task.content = request.form['content']

        try:
             db.session.commit()
             return redirect('/')
        except:
            return 'There is an error'

    else:
        task_to_view = Todo.query.get_or_404(id)
        return render_template('view.html',task=task_to_view)

if __name__=="__main__":
    app.run(debug=True)