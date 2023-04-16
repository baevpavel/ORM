import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json

from models import create_tables, Publisher, Sale, Book, Stock, Shop

SQLsystem = 'postgresql'
login = 'postgres'
password = 'postgres'
host = 'localhost'
port = 5432
db_name = "shopbooks_db"
DSN = f'{SQLsystem}://{login}:{password}@{host}:{port}/{db_name}'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
s = Session()

create_tables(engine)

with open('data.json', 'r') as db:
    data = json.load(db)

for line in data:
    method = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[line['model']]
    s.add(method(**line.get('fields')))

s.commit()

publ_name = input('Ведите имя писателя или id для вывода: ')
if publ_name.isnumeric():
    id = int(publ_name)
else:
    id = s.query(Publisher.id).filter(Publisher.name == publ_name).all()[0][0]
q = s.query(Publisher.name,Shop.name).join(Stock).join(Book).join(Publisher).outerjoin(Sale).filter(Publisher.id == id).order_by(Shop.name)
for i in q:
    print(i)
s.close()