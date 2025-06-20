from flask import Flask, render_template, request # This is to redirect to html page?
from flask_sqlalchemy import SQLAlchemy as sa
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column    
from sqlalchemy import text, Integer, String  # Basically sqlalchemy doesn't recognize anything 
from sqlalchemy.dialects.postgresql import ARRAY # I don't know why arrays aren't built in

app = Flask(__name__)

db = sa(app)

# Connect to my supabase database 
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:supabasetesting@db.uexllsxcfbknokvcdrvr.supabase.co:5432/postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Basic User model that I created
class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = 'User'
    
    id = mapped_column(Integer, primary_key=True, nullable=False)
    username = mapped_column(String, unique=True, nullable=False)
    email = mapped_column(String, nullable=False)
    name = mapped_column(String, nullable=False)
    age = mapped_column(Integer, nullable=False)

# class Student(User):
#     teacherId = db.Column(db.Integer(), primary_key=False)
#     tutorId = db.Column(db.Integer(), primary_key=False)
#     #school = db.Column(db.String(), nullable=False)
#     #classroom = db.Column(db.String(), nullable=False)
#     grade = db.Column(db.Integer(), nullable=False)
#     #subject = db.Column(db.String(), nullable=False)

# class Teacher(User):
#     #school = db.Column(db.String(), nullable=False)
#     subject = db.Column(db.String(), nullable=False)
#     #classroom = db.Column(db.String(), nullable=False)

# class Admin(User):
#     school = db.Column(db.String(), nullable=False)

# class Tutor(User):
#     subjects = db.Column(ARRAY(db.String()), nullable=False, default=[])
#     studentIds = db.Column(ARRAY(db.Integer()), default=[])

# Create tables
with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/test-db')
def test_db():
    try:
        result = sa.session.execute(text("SELECT 1")).scalar()
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

# Additional test route to try creating a user
@app.route('/test',  methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        name = request.form.get('name')
        age = request.form.get('age')
        try:
            # No clue what this does but it works
            #db.session.execute(text("SELECT 1"))
            user = User(username=username, email=email, name=name, age=int(age))
            sa.session.add(user)
            sa.session.commit()
            return "Created new user"
        except Exception as e:
            return f"Error: {str(e)}"
        
    return '''
        <form method="POST">
            Username: <input type="text" name="username"><br>
            Email: <input type="text" name="email"><br>
            Name: <input type="text" name="name"><br>
            Age: <input type="number" name="age"><br>
            <input type="submit" value="Create User">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)