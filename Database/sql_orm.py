from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session

from datetime import datetime

engine = create_engine('sqlite:////web/Sqlite-Data/example.db')

Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer(), primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False)
    email = Column(String(200), nullable=False)
    address = Column(String(200), nullable=False)
    town = Column(String(50), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    orders = relationship("Order", backref='customer')

    def __repr__(self):
        return "<Customer:{0}-{1}>".format(self.id, self.username)


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer(), primary_key=True)
    name = Column(String(200), nullable=False)
    cost_price = Column(Numeric(10, 2), nullable=False)
    selling_price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(SmallInteger(), nullable=False)

    def __repr__(self):
        return "<Item:{0}-{1}>".format(self.id, self.name)


# __table_args__ = (CheckConstraint('quantity > 0', name='quanity_check'),)


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer(), primary_key=True)
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    date_placed = Column(DateTime(), default=datetime.now, nullable=False)
    date_shipped = Column(DateTime())

    # line_items = relationship("OrderLine", secondary="order_lines", backref='order')

    def __ref__(self):
        return "<Order:{0}>".format(self.id)


class OrderLine(Base):
    __tablename__ = 'order_lines'
    id = Column(Integer(), primary_key=True)
    order_id = Column(Integer(), ForeignKey('orders.id'))
    item_id = Column(Integer(), ForeignKey('items.id'))
    quantity = Column(SmallInteger())
    item = relationship("Item")
    order = relationship("Order", backref='order_lines')

    def __repr__(self):
        return "<OrderLine:{0}>".format(self.id)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

c1 = Customer(first_name='Toby',
              last_name='Miller',
              username='tmiller',
              email='tmiller@example.com',
              address='1662 Kinney Street',
              town='Wolfden'
              )

c2 = Customer(first_name='Scott',
              last_name='Harvey',
              username='scottharvey',
              email='scottharvey@example.com',
              address='424 Patterson Street',
              town='Beckinsdale'
              )

# c1,c2

# c1.first_name, c1.last_name
# c2.first_name, c2.last_name

# session.add_all([c1,c2])
# session.commit()

# c1.id,c2.id

# c1.orders, c2.orders

c3 = Customer(first_name='John',
              last_name='Lara',
              username='johnlara',
              email='johnlara.mail.com',
              address='3073 Derek Drive',
              town='Norfolk'
              )

c4 = Customer(first_name='Sarah',
              last_name='Tomlin',
              username='sarahtomlin',
              email='saratomlin@mail.com',
              address='3572 Poplar Avenue',
              town='Norfolk'
              )

c5 = Customer(first_name='John',
              last_name='Green',
              username='johngreen',
              email='johngreen@mail.com',
              address='164 Hidden Valley Road',
              town='Norfolk'
              )

c6 = Customer(first_name='Katherine',
              last_name='Wilson',
              username='katwilson',
              email='katwilson@gmail.com',
              address='4685 West Side Avenue',
              town='Peterbrugh'
              )

session.add_all([c1, c2, c3, c4, c5, c6])
session.commit()

i1 = Item(name='Chair', cost_price=9.21, selling_price=10.81, quantity=5)
i2 = Item(name='Pen', cost_price=3.45, selling_price=4.51, quantity=3)
i3 = Item(name='Headphone', cost_price=15.52, selling_price=16.81, quantity=50)
i4 = Item(name='Travel Bag', cost_price=20.10, selling_price=24.21, quantity=50)
i5 = Item(name='Keyboard', cost_price=20.10, selling_price=22.11, quantity=50)
i6 = Item(name='Monitor', cost_price=200.14, selling_price=212.89, quantity=50)
i7 = Item(name='Watch', cost_price=100.58, selling_price=104.41, quantity=50)
i8 = Item(name='Water Bottle', cost_price=20.89, selling_price=25, quantity=50)

session.add_all([i1, i2, i3, i4, i5, i6, i7, i8])
session.commit()

o1 = Order(customer=c1)
o2 = Order(customer=c1)

order_line1 = OrderLine(order=o1, item=i1, quantity=3)
order_line2 = OrderLine(order=o1, item=i2, quantity=2)
order_line3 = OrderLine(order=o2, item=i1, quantity=1)
order_line4 = OrderLine(order=o2, item=i2, quantity=4)

session.add_all([o1, o2])

session.new
session.commit()

o3 = Order(customer=c1)

orderline1 = OrderLine(item=i1, quantity=5)
orderline2 = OrderLine(item=i2, quantity=10)

o3.order_lines.append(orderline1)
o3.order_lines.append(orderline2)

session.add_all([o3])

session.commit()

c1.orders[0].order_lines, c1.orders[1].order_lines

for ol in c1.orders[0].order_lines:
    ol.id, ol.item, ol.quantity

print('------')

for ol in c1.orders[1].order_lines:
    ol.id, ol.item, ol.quantity

# Querying Data

session.query(Customer).all()

session.query(Item).all()
session.query(Order).all()

print(session.query(Customer))

q = session.query(Customer)
for c in q:
    c.id, c.first_name

session.query(Customer.id, Customer.first_name).all()

## count() method

session.query(Customer).count()
session.query(Item).count()
session.query(Order).count()

# first() method

session.query(Customer).first()
session.query(Item).first()
session.query(Order).first()

## get() method

session.query(Customer).get(1)
session.query(Item).get(1)
session.query(Order).get(100)

## filter() method

(session.query(Customer).filter(Customer.first_name == 'John').all())

print(session.query(Customer).filter(Customer.first_name == 'John'))

session.query(Customer).filter(Customer.id <= 5, Customer.town == "Norfolk").all()
print(session.query(Customer).filter(Customer.id <= 5, Customer.town.like("Nor%")))

from sqlalchemy import or_, and_, not_

# find all customers who either live in Peterbrugh or Norfolk

session.query(Customer).filter(or_(
    Customer.town == 'Peterbrugh',
    Customer.town == 'Norfolk'
)).all()

# find all customers whose first name is John and live in Norfolk

session.query(Customer).filter(and_(
    Customer.first_name == 'John',
    Customer.town == 'Norfolk'
))

# find all Johns who dont live in Peterbrugh

session.query(Customer).filter(and_(
    Customer.first_name == 'John',
    not_(Customer.town == 'Peterbrugh', )
)).all()

# is Null

session.query(Order).filter(Order.date_shipped == None).all()

# Is not null

session.query(Order).filter(Order.date_shipped != None).all()

# In
session.query(Customer).filter(Customer.first_name.in_(['Toby', 'Sarah'])).all()

# Not In
session.query(Customer).filter(Customer.first_name.notin_(['Toby', 'Sarah'])).all()

# Bewteen

session.query(Item).filter(Item.cost_price.between(10, 50)).all()

# NotBetween

session.query(Item).filter(not_(Item.cost_price.between(10, 50))).all()

# Like
session.query(Item).filter(Item.name.like("%r")).all()

session.query(Item).filter(Item.name.ilike("w%")).all()

# Not Like

session.query(Item).filter(not_(Item.name.like("W%"))).all()

# limit() method
session.query(Customer).limit(2).all()
session.query(Customer).filter(Customer.address.ilike("%avenue")).limit(2).all()

print(session.query(Customer).limit(2))
print(session.query(Customer).filter(Customer.address.ilike("%avenue")).limit(2))

# offset() method

session.query(Customer).limit(2).offset(2).all()

print(session.query(Customer).limit(2).offset(2))

# order_by()method

session.query(Item).filter(Item.name.ilike("wa%")).all()

from sqlalchemy import desc

session.query(Item).filter(Item.name.ilike("wa%")).order_by(desc(Item.cost_price)).all()

# join method
session.query(Customer).join(Order).all()
session.query(Customer).join(Order)

session.query(Customer.id, Customer.username, Order.id).join(Order).all()

#session.query(
    #Customer.first_name,
    #Item.name,
    #Item.selling_price,
    #OrderLine.quantity
#).join(Order).join(OrderLine).join(Item).filter(
    #Customer.first_name == 'John',
    #Customer.last_name == 'Green',
    #Order.id == 1,
#).all()

# outerjoin()method

#session.query(
    #Customer.first_name,
    #Order.id,
#).outerjoin(Order).all()

#session.query(
    #Customer.first_name,
    #Order.id,
#).outerjoin(Order, full=True).all()
# got error saying right and full outer joins are currently not supported

# group_by() method
from sqlalchemy import func

session.query(func.count(Customer.id)).join(Order).filter(
    Customer.first_name == 'John',
    Customer.last_name == 'Green',
).group_by(Customer.id).scalar()

# having()method

# finding the number of customers living in each town

print(session.query(
    func.count("*").label('town_count'),
    Customer.town
).group_by(Customer.town).having(func.count("*") > 90).all())

##Dealing with Duplicates

from sqlalchemy import distinct

session.query(Customer.town).filter(Customer.id < 10).all()

session.query(Customer.town).filter(Customer.id < 10).distinct().all()

print(session.query(
    func.count(distinct(Customer.town)),
    func.count(Customer.town)
).all())

##Casting

from sqlalchemy import cast, Date, union

session.query(
    cast(func.pi(), Integer),
    cast(func.pi(), Numeric(10,2)),
    cast(datetime(2010,12, 1)),
    cast(datetime(2010,12, 1)),
).all()

