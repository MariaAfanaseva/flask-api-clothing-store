from db import db
from models.product import Product

menu_products = db.Table('menu_products',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('menu_id', db.Integer, db.ForeignKey('menu.id'), primary_key=True)
)


class MenuItem(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(80), nullable=False, unique=True)
    image_url = db.Column(db.String(128))
    size = db.Column(db.String(80))
    link_url = db.Column(db.String(128))
    products = db.relationship('Product', secondary=menu_products, lazy='subquery',
                               backref=db.backref('menu', lazy=True))

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
            'items': [self.products[i].json() for i in range(quantity)]
        }

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
