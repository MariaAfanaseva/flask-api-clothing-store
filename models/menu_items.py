from db import db


class MenuItemsModel(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    image_url = db.Column(db.String(128))
    size = db.Column(db.String(80))
    link_url = db.Column(db.String(128))

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

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
