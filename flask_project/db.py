import sqlalchemy as sql
import sqlalchemy.orm as sql_orm

import os


DBMS = 'postgresql'
DB_HOST_ADDR = os.getenv('POSTGRESQL_HOST_ADDR', '127.0.0.1')
DB_HOST_PORT = os.getenv('POSTGRESQL_HOST_PORT', '5432')
DB_USER = os.getenv('POSTGRESQL_USER', 'test')
DB_PWD = os.getenv('POSTGRESQL_PWD', 'test')
DB_NAME = os.getenv('POSTGRESQL_DB', 'test')

DSN = \
    f'{DBMS}://{DB_USER}:{DB_PWD}@{DB_HOST_ADDR}:{DB_HOST_PORT}/{DB_NAME}'

engine = sql.create_engine(DSN)

BaseClass = sql_orm.declarative_base()


class User(BaseClass):
    __tablename__ = 'user'

    id = sql.Column(sql.Integer, primary_key=True)
    created = sql.Column(sql.DateTime, server_default=sql.func.now())
    email = sql.Column(sql.String(length=40), nullable=False, unique=True)
    pwd_hash = sql.Column(sql.String(length=50), nullable=False)


class Advertisement(BaseClass):
    __tablename__ = 'advertisement'

    id = sql.Column(sql.Integer, primary_key=True)
    created = sql.Column(sql.DateTime, server_default=sql.func.now())
    title = sql.Column(sql.String(length=50), nullable=False)
    description = sql.Column(sql.Text)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey('user.id'))

    owner = sql_orm.relationship(User, backref='advertisement')

    def to_dict(self):
        return \
            {fld.name:getattr(self, fld.name) for fld in self.__table__.c}


BaseClass.metadata.create_all(engine)


def create_adv(data: dict):
    Session = sql_orm.sessionmaker(bind=engine)
    with Session() as session:
        adv = Advertisement(**data)
        session.add(adv)
        session.commit()
        new_adv_id = adv.id
    return new_adv_id

def get_adv(adv_id: int):
    Session = sql_orm.sessionmaker(bind=engine)
    with Session() as session:
        adv = session.get(Advertisement, adv_id)
    return adv

def delete_adv(adv_id: int) -> bool:
    Session = sql_orm.sessionmaker(bind=engine)
    with Session() as session:
        adv = get_adv(adv_id)
        if not adv:
            return False
        session.delete(adv)
        session.commit()
    return True
