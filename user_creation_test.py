from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import create_engine, String, Text, select, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, mapped_column, Mapped, Session, relationship
from flask import Flask, render_template, request
from typing import List

engine = create_engine("postgresql://postgres:supabasetesting@db.uexllsxcfbknokvcdrvr.supabase.co:5432/postgres", echo = True)

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_type: Mapped[str]
    district: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    age: Mapped[Optional[int]] = mapped_column(String, nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)


    __mapper_args__ = {
        "polymorphic_identity": "User",
        "polymorphic_on": "user_type",
    }
    
    def __repr__(self):
        return f"User(id={self.id}, name={self.username})"
    
class User_Login(Base):
    __tablename__ = "user_login"
    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    
class Tutor(User):
    __tablename__ = "tutor"
    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    subjects: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    students: Mapped[List["Student"]] = relationship(
        back_populates="tutor", 
        foreign_keys="Student.tutor_id"
    )

    __mapper_args__ = {
        "polymorphic_identity": "Tutor",
    }

    def __repr__(self):
        return f"Tutor(id={self.id}, username={self.username})"


class Student(User):
    __tablename__ = "student"
    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    teacher_id: Mapped[Optional[int]]
    tutor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tutor.id"), nullable=True)
    grade: Mapped[Optional[int]]
    stored_chats: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    staring_assessment: Mapped[Optional[int]]
    current_subject: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    progress_percentage: Mapped[Optional[float]]

    tutor: Mapped[Optional["Tutor"]] = relationship(
        back_populates="students",
        foreign_keys=[tutor_id]
    )

    __mapper_args__ = {
        "polymorphic_identity": "Student",
    }

    def __repr__(self):
        return f"Student(id={self.id}, username={self.username})"

""" class Post(Base):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), default="Untitled Post")
    content: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="posts")

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title})" """

Base.metadata.create_all(engine)

# with Session(engine) as session:
#     anthony = User(name="Anthony")
#     kim = User(name="Kim", last_login=datetime.now(timezone.utc))
#     session.add(anthony)
#     session.add(kim)
#     session.commit()

#     post1 = Post(title="Anthony's first post", content="Hello world!")
#     post2 = Post(title="Kim's first post", content="Hello again!")
#     post3 = Post(title="Anthony's second post", content="Hello world!")
#     post4 = Post(title="Anthony's third post", content="Hello again!")
#     post5 = Post(title="Kim's second post", content="Hello again!")

#     anthony.posts.append(post1)
#     anthony.posts.append(post3)
#     anthony.posts.append(post4)
#     kim.posts.append(post2)
#     kim.posts.append(post5)

#     session.commit()

#     stmt = select(User)
#     users = session.scalars(stmt).all()
#     for user in users:
#         print(user)
#         for post in user.posts:
#             print(f"  {post}")

#     anthony = session.get(User, 1)
#     if anthony:
#         print(f"Found user: {anthony}")

#     stmt = select(User).where(User.name == "Kim")
#     kim = session.scalars(stmt).first()
#     if kim:
#         print(f"Found user: {kim}")

#     stmt = select(Post).where(Post.user == anthony).order_by(Post.id.desc())
#     posts = session.scalars(stmt).all()
#     for post in posts:
#         print(post)
#         print(f"  {post.user}")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        try:
            with Session(engine) as session:
                user_login = session.query(User_Login).filter_by(username=request.form.get('username')).first()
                if user_login:
                    return "Username already exists. Please choose a different username."
                user = User(
                    user_type=request.form.get('user_type'),
                    name = request.form.get('name'),
                    district = request.form.get('district'),
                    age = request.form.get('age')
                )
                session.add(user)
                session.commit()
                user2 = User_Login(id=user.id, username=request.form.get('username'), password=request.form.get('password'))
                session.add(user2)
                session.commit()
                if request.form.get('user_type') == 'Tutor':
                    tutor = Tutor(id=user.id, subjects=request.form.get('subjects'))
                    session.add(tutor)
                    session.commit()
                elif request.form.get('user_type') == 'Student':
                    student = Student(id=user.id, teacher_id=request.form.get('teacher_id'), tutor_id=request.form.get('tutor_id'), grade=request.form.get('grade'), stored_chats=request.form.get('stored_chats'), staring_assessment=request.form.get('staring_assessment'), current_subject=request.form.get('current_subject'), progress_percentage=request.form.get('progress_percentage'))
                    session.add(student)
                    session.commit()
            return f"User created successfully!"
        except Exception as e:
            return f"Error: {str(e)}"
    return "User created"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        with Session(engine) as session:
            user_login = session.query(User_Login).filter_by(username=username, password=password).first()
            if user_login:
                return f"Login successful for user: {user_login.username} with ID: {user_login.id}"
            else:
                return "Invalid username or password"
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)