import json
from app import Teacher, db, app


def seed(teachers):
    with app.app_context():
        for teacher_data in teachers:
            teacher = Teacher(
                name=teacher_data['name'], about=teacher_data['about'],
                rating=teacher_data['rating'], picture=teacher_data['picture'],
                price=teacher_data['price'], goals=teacher_data['goals'],
                free=teacher_data['free']
            )
            db.session.add(teacher)
        db.session.commit()


def main():
    with open('data.json', encoding='utf-8') as f:
        teachers = json.load(f)
    seed(teachers)


if __name__ == '__main__':
    main()
