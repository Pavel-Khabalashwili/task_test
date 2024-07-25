from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import random
from faker import Faker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://admin:admin@postgresql:5432/skillbox_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
fake = Faker()

class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    breed = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    age_in_months = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.Index('idx_cat_fulltext', 'breed', 'name', 'description', 'age_in_months'),
    )

def populate_data():
    """Функция для заполнения таблицы данными"""
    images = [
        'static/images/1.jpg',
        'static/images/2.jpg',
        'static/images/3.jpg',
        'static/images/4.jpg',
        'static/images/5.jpg'
    ]
    object_list = []
    for _ in range(20):
        object_list.append(Cat(
            breed=fake.word(),
            image=random.choice(images),
            name=fake.first_name(),
            description=fake.text(),
            age_in_months=random.randint(1, 36)
        ))
    try:
        with app.app_context():
            db.session.bulk_save_objects(object_list)
            db.session.commit()
    except IntegrityError:
        db.session.rollback()

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    query = request.args.get('query', '')
    sort_by = request.args.get('sort_by', 'relevance')
    page = request.args.get('page', 1, type=int)

    cats_query = Cat.query

    if query:
        search = f"%{query}%"
        cats_query = cats_query.filter(
            db.or_(
                Cat.breed.ilike(search),
                Cat.name.ilike(search),
                Cat.description.ilike(search),
                db.cast(Cat.age_in_months, db.String).ilike(search)
            )
        )

    if sort_by == 'breed':
        cats_query = cats_query.order_by(Cat.breed)
    elif sort_by == 'age':
        cats_query = cats_query.order_by(Cat.age_in_months)
    else:
        cats_query = cats_query.order_by(Cat.id)

    cats = cats_query.paginate(page=page, per_page=5, error_out=False)
    return render_template('index.html', cats=cats, query=query, sort_by=sort_by)


@app.route('/cat/<int:cat_id>')
def cat_detail(cat_id):
    cat = Cat.query.get_or_404(cat_id)
    return render_template('cat_detail.html', cat=cat)

if __name__ == '__main__':
    create_tables()
    populate_data()
    app.run(host='0.0.0.0', port=5000, debug=True)
