from flask import Flask, render_template, abort, request, redirect, url_for
from data import goals, week, emodji
import json
import random
from operator import itemgetter

app = Flask(__name__)


@app.route('/')
def index():
    with open('data.json', 'r', encoding='utf-8') as f:
        teachers = random.choices(json.load(f), k=6)
        return render_template('index.html', teachers=teachers)


@app.route('/all', methods=['GET', 'POST'])
def all():
    with open('data.json', 'r', encoding='utf-8') as f:
        teachers = json.load(f)
    if request.method == 'POST':
        req = request.form['select']
        if req == 'random':
            random.shuffle(teachers)
        elif req == 'rating':
            teachers.sort(key=itemgetter('rating'), reverse=True)

        elif req == 'high':
            teachers.sort(key=itemgetter('price'), reverse=True)

        elif req == 'low':
            teachers.sort(key=itemgetter('price'))

        return render_template('all.html', teachers=teachers, req=req)
    random.shuffle(teachers)
    return render_template('all.html', teachers=teachers)


@app.route('/goals/<goal>')
def goal(goal):
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            teachers = json.load(f)
            teachers_by_goal = []
            for teacher in teachers:
                if goal in teacher['goals']:
                    teachers_by_goal.append(teacher)

            return render_template('goal.html', goal=goal, goals=goals, emodji=emodji, teachers=teachers_by_goal)
    except Exception as e:
        abort(404, e)


@app.route('/profiles/<int:id>')
def profile(id):
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            teacher = json.load(f)[id]
            return render_template('profile.html', teacher=teacher, week=week, id=id)
    except Exception:
        abort(404)


@app.route('/request')
def request_teacher():
    return render_template('request.html')


@app.route('/request_done')
def request_done():
    req = request.args.to_dict()
    try:
        with open('request.json', 'r', encoding='utf-8') as f:
            file = json.load(f)
            file.append(req)

    except (json.decoder.JSONDecodeError, FileNotFoundError):
        file = [req]

    with open('request.json', 'w+', encoding='utf-8') as f:
        json.dump(file, f, ensure_ascii=False, indent=2)

    return render_template('request_done.html', goals=goals, req=req)


@app.route('/booking/<int:id>/<day>/<time>', methods=['GET', 'POST'])
def form(id, day, time):
    if request.method == 'POST':

        request_detail = request.form.to_dict()
        name = request_detail['clientName']
        tel = request_detail['clientPhone']
        try:
            with open('booking.json', 'r', encoding='utf-8') as f:
                file = json.load(f)
                file.append(request_detail)

        except (json.decoder.JSONDecodeError, FileNotFoundError):
            file = [request_detail]

        with open('booking.json', 'w+', encoding='utf-8') as f:
            json.dump(file, f, ensure_ascii=False, indent=2)

        return redirect(url_for('booking_done', day=day, time=time, name=name, tel=tel))

    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            teacher = json.load(f)[id]
            return render_template('booking.html', id=id, day=day, time=time, teacher=teacher, week=week)
    except Exception:
        abort(404)


@app.route('/booking-done/<day>/<time>/<name>/<tel>')
def booking_done(day, time, name, tel):
    return render_template('booking_done.html', day=week[day], time=time, name=name, tel=tel)


if __name__ == '__main__':
    app.run()
