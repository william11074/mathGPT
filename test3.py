from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import create_engine, String, Text, select, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, mapped_column, Mapped, Session, relationship
from flask import Flask, render_template, request

engine = create_engine("postgresql://postgres:supabasetesting@db.uexllsxcfbknokvcdrvr.supabase.co:5432/postgres", echo = True)

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    user_type: Mapped[str] = mapped_column(String(30))

    def __repr__(self):
        return f"User(id={self.id}, name={self.username})"

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
                user = User(
                    username="tester",
                    user_type="tester"
                )
                session.add(user)
                session.commit()
            return f"User created successfully!"
        except Exception as e:
            return f"Error: {str(e)}"
    return "User created"