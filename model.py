from sqlalchemy import create_engine, Column, String, Integer, BigInteger, Date, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('postgres://postgres:03rod06ion01@localhost:5432/lab1')
Base = declarative_base()


class Account(Base):
    __tablename__ = 'account'

    account_id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    created = Column(Date)

    games = relationship("Game")

    def __init__(self, login=None, password=None, created=None):
        self.login = login
        self.password = password
        self.created = created


class Game(Base):
    __tablename__ = 'game'

    game_id = Column(Integer, primary_key=True)
    game_name = Column(String)
    hours_played = Column(Integer)
    account = Column(Integer, ForeignKey('account.account_id'))

    items = relationship("Item")

    def __init__(self, game_name=None, hours_played=None, account=None):
        self.game_name = game_name
        self.hours_played = hours_played
        self.account = account


class Item(Base):
    __tablename__ = 'item'

    item_id = Column(Integer, primary_key=True)
    item_name = Column(String)
    price = Column(Numeric)
    game = Column(Integer, ForeignKey('game.game_id'))

    def __init__(self, item_name=None, price=None, game=None):
        self.item_name = item_name
        self.price = price
        self.game = game


session = sessionmaker(engine)()
Base.metadata.create_all(engine)

TABLES = {'account': Account, 'game': Game, 'item': Item}


class Model:
    def pairs_from_str(self, string):
        lines = string.split(',')
        pairs = {}

        for line in lines:
            key, value = line.split('=')
            pairs[key.strip()] = value.strip()
        return pairs

    def filter_by_pairs(self, objects, pairs, cls):
        for key, value in pairs.items():
            field = getattr(cls, key)
            objects = objects.filter(field == value)
        return objects

    def get(self, tname, condition):

        object_class = TABLES[tname]
        objects = session.query(object_class)

        if condition:
            try:
                pairs = self.pairs_from_str(condition)
            except Exception as err:
                raise Exception('Incorrect input')
            objects = self.filter_by_pairs(objects, pairs, object_class)

        return list(objects)

    def insert(self, tname, columns, values):
        columns = [c.strip() for c in columns.split(',')]
        values = [v.strip() for v in values.split(',')]

        pairs = dict(zip(columns, values))
        object_class = TABLES[tname]
        obj = object_class(**pairs)

        session.add(obj)

    def commit(self):
        session.commit()

    def delete(self, tname, condition):
        pairs = self.pairs_from_str(condition)
        object_class = TABLES[tname]

        objects = session.query(object_class)
        objects = self.filter_by_pairs(objects, pairs, object_class)

        objects.delete()

    def update(self, tname, condition, statement):
        pairs = self.pairs_from_str(condition)
        new_values = self.pairs_from_str(statement)
        object_class = TABLES[tname]

        objects = session.query(object_class)
        objects = self.filter_by_pairs(objects, pairs, object_class)

        for obj in objects:
            for field_name, value in new_values.items():
                setattr(obj, field_name, value)

    def fill_account_with_random_data(self):
        sql = """
            CREATE OR REPLACE FUNCTION randomAccounts()
                RETURNS void AS $$
            DECLARE
                step integer  := 0;
            BEGIN
                LOOP EXIT WHEN step > 10000;
                    INSERT INTO account (login, password, created)
                    VALUES (
                        substring(md5(random()::text), 1, 10),
                        substring(md5(random()::text), 1, 10),
            			timestamp '2014-01-10 20:00:00' + random() * (timestamp '2020-12-30 20:00:00' - timestamp '2014-01-10 10:00:00'));
            			step := step + 1;
                END LOOP ;
            END;
            $$ LANGUAGE PLPGSQL;
            SELECT randomAccounts();
            """
        try:
            session.execute(sql)
        finally:
            session.commit()
