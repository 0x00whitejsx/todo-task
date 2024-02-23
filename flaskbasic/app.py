from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Todo.db"
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        todo_title = request.form["title"]
        todo_desc = request.form["desc"]
        data = Todo(title=todo_title, desc=todo_desc)
        db.session.add(data)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template("index.html", alltodo=alltodo)


@app.route("/show")
def show():
    alltodo = Todo.query.all()
    return render_template("show.html", alltodo=alltodo)


@app.route("/delete/<int:sno>")
def taskDelete(sno):
    todo_data = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo_data)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
