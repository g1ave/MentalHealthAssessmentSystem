from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(config)  # 从config导入配置文件
db = SQLAlchemy(app)


class Assitant(db.Model):
    __tablename__ = 'assitant'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True)
    passwd = db.Column(db.String(80))
    phone = db.Column(db.String(120), index=True)

    def __repr__(self):
        return '<Username %r, PhoneNumber:%r>' % (self.username, self.phone)


class Customer(db.Model):
    __tablename__ = 'TableCustomer'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True)
    name = db.Column(db.Text(80), index=True)
    gender = db.Column(db.Text(20))
    phoneNumber = db.Column(db.Integer)
    score = db.Column(db.Integer)
    career = db.Column(db.String(80))
    email = db.Column(db.String(120))
    passwd = db.Column(db.String(80))

    def __repr__(self):
        return '<Username %r, score:%d>' % (self.username, self.score)


@app.route('/sys', methods=['GET', 'POST'])
def index():
    f =  open('question.txt', 'r')
    str_file = f.read()
    qa, qb, Res = str_file.split('\n\n\n')
    Res = Res.split('\n')
    if request.method == 'POST':
        res = 0
        for i in range(20):
            index = 'options' + str(i)
            res += int(request.form[index])
        for i in range(5):
            index = 'sel' + str(i)
            res += int(request.form[index])
        username = session.get('name')
        user = Customer.query.filter_by(username=username).first()
        user.score = res
        db.session.add(user)
        db.session.commit() 
        flash('您的分数:{}\n您的评估是:{}'.format(res,Res[res//8]))
        return redirect(url_for('index'))  
    QuesA = []
    QuesB = []
    BasicQuestions = qa.split('\n\n')
    for index, BasicQuestion in enumerate(BasicQuestions):
        ques, optionA, optionB, optionC = BasicQuestion.split()
        QuesA.append({
            'id' : index,
            'ques':ques,
            'optionA' : optionA,
            'optionB' : optionB,
            'optionC' : optionC,
        })
    SpecialQuestions = qb.split('\n\n')
    for index, SpecialQuestion in enumerate(SpecialQuestions):
        ques, optionA, optionB, optionC = SpecialQuestion.split()
        QuesB.append({
            'id' : index,
            'ques' : ques,
            'optionA' : optionA,
            'optionB' : optionB,
            'optionC' : optionC,
        })
    return render_template('index.html', BasicQuestions=QuesA, SpecialQuestion=QuesB, name=session.get('name'))

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['passwd']
        option = request.form['options']
        if option == 'customer':
            user = Customer.query.filter_by(username=username).first()
            if user is not None and user.passwd == passwd:
                 session['name'] = username
                 return redirect(url_for('index'))
            else:
                flash('用户名或密码错误')
                return redirect(url_for('login'))
        elif option == 'assitant':
            assitant = Assitant.query.filter_by(username=username).first()
            if assitant is not None and assitant.passwd == passwd:
                return redirect(url_for('manageCustomer'))
            else:
                flash('用户名或密码错误')
                return redirect(url_for('login'))
        else:
            if username == 'root' and passwd == 'admin':
                return redirect('/assitant')
            else:
                flash('用户名或密码错误！')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/assitant', methods=['GET', 'POST'])
def admin():
    db.create_all()
    if request.method == 'POST':
        username = request.form['username']
        phone = request.form['phone']
        passwd = request.form['passwd']
        option = request.form['options']
        if option == 'addUser':
            newuser = Assitant(username=username, phone=phone, passwd=passwd)
            db.session.add(newuser)
            db.session.commit()
        elif option == 'queryUser':
            users = Assitant.query.filter_by(username=username).all()
            return render_template('assitant.html', users=users)
        elif option == 'changeUser':
            user = Assitant.query.filter_by(username=username).first()
            user.phone = phone
            user.passwd = passwd
            db.session.add(user)
            db.session.commit()
        else:
            user = Assitant.query.filter_by(username=username).first()
            db.session.delete(user)
            db.session.commit()
        return redirect('/assitant')
    else:
        users = Assitant.query.all()
        return render_template('assitant.html', users=users)


@app.route('/customer',  methods=['GET', 'POST'])
def manageCustomer():
    db.create_all()
    if request.method == 'POST':
        name = request.form['realname']
        username = request.form['username']
        gender = request.form['gender']
        phone = request.form['phonenumber']
        career = request.form['career']
        email = request.form['email']
        option = request.form['options']
        passwd = request.form['passwd']
        if option == 'addCustomer':
            newuser = Customer( username=username, 
                                email=email,
                                name=name,
                                phoneNumber=phone,
                                career=career,
                                gender=gender,
                                passwd=passwd)
            db.session.add(newuser)
            db.session.commit()
        else:
            user = Customer.query.filter_by(username=username).first()
            user.email = email
            user.phoneNumber = phone
            user.passwd = passwd
            db.session.add(user)
            db.session.commit()
        return redirect('/customer')
    else:
        users = Customer.query.all()
    return render_template('customer.html', customers=users)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
