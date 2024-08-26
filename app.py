#imports

from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
Scss(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    # created = db.Column(db.datetime)
    
    def __repr__(self) -> str:
        return f"Task {self.id}"


@app.route("/", methods=["GET", "POST"])
def index():
    
    if request.method == "POST":
        current_task = request.form['content']
        
        new_task = Task(content=current_task)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            
            return redirect('/')
        except Exception as er:
            print(f"Error {er}")
            return f"Error {er}"
    
    else:
        tasks = Task.query.order_by(Task.id).all()
        return render_template('index.html', tasks=tasks)
        
    return render_template("index.html")

@app.route('/delete/<int:id>')
def delete(id:int):
    delete_task = Task.query.get_or_404(id)
    
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as er:
            print(f"Error {er}")
            return f"Error {er}"


@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edi(id:int):
    task = Task.query.get_or_404(id)
    
    if request.method == "POST":
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect("/")
        except Exception as er:
                print(f"Error {er}")
                return f"Error {er}"

    else:
        return render_template('edit.html', task=task)

if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)