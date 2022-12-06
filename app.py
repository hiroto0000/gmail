from flask import Flask, render_template, request, redirect, session
from helper import mail, reply_mail
import secrets
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Sequence
from sqlalchemy.orm import declarative_base, sessionmaker



app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# -------------------------------------------------------------------
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)
# ---------------------------------------------------------------------

engine = create_engine('sqlite:///mail.db', echo=False)
Base = declarative_base()

class Mail(Base):
    __tablename__ = 'mails'
    id = Column(Integer, Sequence("id"), primary_key=True)
    email = Column(String)
    subject = Column(String)
    body = Column(String)
    date = Column(DateTime, default=datetime.now)

@app.route('/', methods=["GET", "POST"])
def index():
    """
    GET:index.htmlの表示
    POST:メールの送信
    """
    if request.method == 'POST':
        subject = request.form.get("subject")
        text = request.form.get("text")
        email = request.form.get("email")
        # print(subject)
        # print(text)
        a = mail(subject, text)

        Session = sessionmaker(bind=engine)
        session = Session()
        user_a = Mail(email=email, subject=subject, body=text)
        session.add(user_a)
        session.commit()
        if a:
            return render_template("thanks.html")
        else:
        # print(a)
            return redirect("/")
    
    else:
        return render_template("index.html")

@app.route("/list")
def list():
    maillist = []
    Session = sessionmaker(bind=engine)
    session = Session()
    for r in session.query(Mail):
        m = {}
        m["id"] = r.id
        m["email"] = r.email
        m["subject"] = r.subject
        m["body"] = r.body
        m["date"] = r.date
        maillist.append(m)
        m["date"] = str(m["date"]).split(".")[0]
    # print(maillist[2][3])
    session.commit()


    return render_template("list.html", contents=maillist)

@app.route("/reply/<int:id>", methods=["GET", "POST"])
def reply(id):
    """
    GET:メールのフォームを提示
    POST:replyのメールを返す
    """
    if request.method == "POST":
        text = request.form.get("body")
        email = request.form.get("email")
        subject = request.form.get("subject")
        reply_mail(email, subject, text)
        return redirect("/")


    else:
        sends = {}
        Session = sessionmaker(bind=engine)
        session = Session()
        rs = session.query(Mail).filter(Mail.id == id).all()
        for r in rs:
            # print(r.id, r.email) 
            sends["email"] = r.email
            sends["subject"] = r.subject
            sends["text"] = r.body 
        print(sends)  
        return render_template("reply.html", sends=sends)

        # print(maillist[2][3])


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1')
