from db import db


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    image_url = db.Column(db.String(128))
    price = db.Column(db.Float(precision=2))

    def __init__(self, name, image_url, price):
        self.name = name
        self.image_url = image_url
        self.price = price

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'imageUrl': self.image_url,
            'price': self.price,
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
