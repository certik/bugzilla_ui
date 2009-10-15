from sqlalchemy import (Table, Column, Integer, String, MetaData, ForeignKey,
        create_engine)
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Bugs(Base):
    __tablename__ = "bugs"

    bug_id = Column(Integer, primary_key=True)
    product_id = Column(Integer)

    def __init__(self, bug_id, product_id):
        self.bug_id = bug_id
        self.product_id = product_id

    def __repr__(self):
        return "<Bugs bug_id=%d, product_id=%d>" % (self.bug_id,
                self.product_id)

class Longdescs(Base):
    __tablename__ = "longdescs"

    bug_id = Column(Integer, primary_key=True)
    thetext = Column(String)

    def __init__(self, bug_id, thetext):
        self.bug_id = bug_id
        self.thetext = thetext

    def __repr__(self):
        return "<Longdescs bug_id=%d>" % (self.bug_id)


engine = create_engine("mysql://bugzilla:pass@localhost/bugzilla",
        echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def show_bug(bug):
    desc = session.query(Longdescs).filter(Longdescs.bug_id==bug.bug_id).one()
    print desc

print "bugs 116:"
bug = session.query(Bugs).filter(Bugs.bug_id==116).one()
show_bug(bug)
