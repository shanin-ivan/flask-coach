from flask import Flask, render_template, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from data import goals, week, emodji
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://xebrtwjlkifehn' \
                                        ':75f4586d8a74e7534c813303e74a7d26b4a57c4c5d9e72308b31d2afb648eba5@' \
                                        'ec2-52-208-164-5.eu-west-1.compute.amazonaws.com:5432/dbj23a6618tgcd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    about = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    goals = db.Column(db.ARRAY(db.String), nullable=False)
    free = db.Column(db.JSON, nullable=False)
    bookings = db.relationship('Booking', back_populates='teacher')


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weekday = db.Column(db.String(10), nullable=False)
    time = db.Column(db.Time, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    client_name = db.Column(db.String(50), nullable=False)
    client_phone = db.Column(db.String(50), nullable=False)
    teacher = db.relationship('Teacher', back_populates='bookings', uselist=False)


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(15), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    tel = db.Column(db.String(50), nullable=False)


@app.route('/')
def index():
    teachers = db.session.query(Teacher).order_by(db.func.random()).limit(6)
    return render_template('index.html', teachers=teachers)
    # with open('data.json', 'r', encoding='utf-8') as f:
    #     teachers = random.choices(json.load(f), k=6)


@app.route('/all', methods=['GET', 'POST'])
def all():
    if request.method == 'POST':
        req = request.form['select']
        if req == 'random':
            teachers = db.session.query(Teacher).order_by(db.func.random()).all()

        elif req == 'rating':
            teachers = db.session.query(Teacher).order_by(Teacher.rating.desc()).all()

        elif req == 'high':
            teachers = db.session.query(Teacher).order_by(Teacher.price.desc()).all()

        elif req == 'low':
            teachers = db.session.query(Teacher).order_by(Teacher.price).all()
        else:
            teachers = db.session.query(Teacher).all()

        return render_template('all.html', teachers=teachers)
    teachers = db.session.query(Teacher).all()
    return render_template('all.html', teachers=teachers)

    # with open('data.json', 'r', encoding='utf-8') as f:
    #     teachers = json.load(f)
    # if request.method == 'POST':
    #     req = request.form['select']
    #     if req == 'random':
    #         random.shuffle(teachers)
    #
    #     elif req == 'rating':
    #         teachers.sort(key=itemgetter('rating'), reverse=True)
    #
    #     elif req == 'high':
    #         teachers.sort(key=itemgetter('price'), reverse=True)
    #
    #     elif req == 'low':
    #         teachers.sort(key=itemgetter('price'))
    #
    #     return render_template('all.html', teachers=teachers, req=req)
    # random.shuffle(teachers)
    # return render_template('all.html', teachers=teachers)


@app.route('/goals/<goal>')
def goal(goal):
    teachers = db.session.query(Teacher).filter(Teacher.goals.any(goal)).all()
    return render_template('goal.html', teachers=teachers, goal=goal, goals=goals, emodji=emodji)

    # try:
    #     with open('data.json', 'r', encoding='utf-8') as f:
    #         teachers = json.load(f)
    #         teachers_by_goal = [teacher for teacher in teachers if goal in teacher['goals']]
    #
    #         return render_template('goal.html', goal=goal, goals=goals, emodji=emodji, teachers=teachers_by_goal)
    # except Exception as e:
    #     abort(404, e)


@app.route('/profiles/<int:id>')
def profile(id):
    teacher = db.session.query(Teacher).get_or_404(id)
    return render_template('profile.html', teacher=teacher, week=week, id=id)
    # with open('data.json', 'r', encoding='utf-8') as f:
    #     teacher = json.load(f)[id]
    #     return render_template('profile.html', teacher=teacher, week=week, id=id)


@app.route('/request')
def request_teacher():
    return render_template('request.html')


@app.route('/request_done')
def request_done():
    req = request.args.to_dict()
    request_form = Request(goal=req['goal'], time=req['time'], name=req['name'], tel=req['tel'])
    db.session.add(request_form)
    try:
        db.session.commit()
    except Exception:
        abort(404)
    return render_template('request_done.html', goals=goals, req=req)

    # req = request.args.to_dict()
    # try:
    #     with open('request.json', 'r', encoding='utf-8') as f:
    #         file = json.load(f)
    #         file.append(req)
    #
    # except (json.decoder.JSONDecodeError, FileNotFoundError):
    #     file = [req]
    #
    # with open('request.json', 'w+', encoding='utf-8') as f:
    #     json.dump(file, f, ensure_ascii=False, indent=2)
    #
    # return render_template('request_done.html', goals=goals, req=req)


@app.route('/booking/<int:id>/<day>/<time>')
def form(id, day, time):
    teacher = db.session.query(Teacher).get_or_404(id)
    return render_template('booking.html', id=id, day=day, time=time, teacher=teacher, week=week)


@app.route('/booking-done', methods=['POST'])
def booking_done():
    req = request.form.to_dict()
    booking = Booking(weekday=req['weekday'], time=req['time'], teacher_id=req['teacher_id'],
                      client_name=req['name'], client_phone=req['phone'])
    db.session.add(booking)
    try:
        db.session.commit()
    except Exception:
        abort(500)

    return render_template(
        'booking_done.html', day=week[req['weekday']], time=req['time'],
        name=req['name'], tel=req['phone']
    )


if __name__ == '__main__':
    app.run()
