from sqlalchemy import (Table, Column, Integer, String, MetaData, ForeignKey,
        create_engine)
from sqlalchemy.orm import mapper, sessionmaker

class Bugs(object):
    def __init__(self, bug_id, product_id):
        self.bug_id = bug_id
        self.product_id = product_id

    def __repr__(self):
        return "<Bugs bug_id=%d, product_id=%d>" % (self.bug_id,
                self.product_id)

metadata = MetaData()
bugs_table = Table("bugs", metadata,
        Column("bug_id", Integer, primary_key=True),
        #Column("short_desc", String),
        Column("product_id", Integer),
        )
engine = create_engine("mysql://bugzilla:4Y7ZkdfBXP4D@localhost/bugzilla",
        echo=True)
metadata.create_all(engine)
mapper(Bugs, bugs_table)
Session = sessionmaker(bind=engine)
session = Session()
print "all bugs:"
print session.query(Bugs).all()
