from databases.db import db
from models.product import Product

menu_products = db.Table('menu_products',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('menu_id', db.Integer, db.ForeignKey('menu_items.id'), primary_key=True)
)


class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=True)
    image_url = db.Column(db.String(128))
    size = db.Column(db.String(80))
    link_url = db.Column(db.String(128))
    products = db.relationship('Product', secondary=menu_products, lazy='dynamic',
                               backref=db.backref('menu_items', lazy=True))

    def __init__(self, title, imageUrl, size, linkUrl):
        self.title = title
        self.image_url = imageUrl
        self.size = size
        self.link_url = linkUrl

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'imageUrl': self.image_url,
            'size': self.size,
            'linkUrl': self.link_url,
        }

    def json_with_products(self, quantity):
        return {
            'id': self.id,
            'title': self.title,
            'linkUrl': self.link_url,
            'items': [product.json() for product in self.products.limit(quantity).all()]
        }

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, number):
        return cls.query.filter_by(id=number).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
