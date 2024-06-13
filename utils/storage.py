import shelve


class Storage:
    def __init__(self, filename='storage.db'):
        self.filename = filename

    def save(self, key, value):
        with shelve.open(self.filename) as db:
            db[key] = value

    def load(self, key, default=None):
        with shelve.open(self.filename) as db:
            return db.get(key, default)

    def delete(self, key):
        with shelve.open(self.filename) as db:
            if key in db:
                del db[key]

    def clear(self):
        with shelve.open(self.filename) as db:
            db.clear()
