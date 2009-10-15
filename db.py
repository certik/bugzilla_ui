from sqlalchemy import (Table, Column, Integer, String, MetaData, ForeignKey,
        DateTime, create_engine)
from sqlalchemy.orm import mapper, sessionmaker, relation
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Longdescs(Base):
    __tablename__ = "longdescs"

    bug_id = Column(Integer, ForeignKey("bugs.bug_id"))
    thetext = Column(String)
    bug_when = Column(DateTime, primary_key=True)


    def __init__(self, bug_id, thetext):
        self.bug_id = bug_id
        self.thetext = thetext

    def __repr__(self):
        return "<Longdescs bug_id=%d>" % (self.bug_id)

class Bugs(Base):
    __tablename__ = "bugs"

    bug_id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    longdescs = relation(Longdescs, backref="longdescs")

    def __init__(self, bug_id, product_id):
        self.bug_id = bug_id
        self.product_id = product_id

    def __repr__(self):
        return "<Bugs bug_id=%d, product_id=%d>" % (self.bug_id,
                self.product_id)



engine = create_engine("mysql://bugzilla:pass@localhost/bugzilla",
        echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def show_bug(bug):
    desc = bug.longdescs
    #desc = session.query(Longdescs).filter(Longdescs.bug_id==bug_id).all()
    print "s"
    print desc

print "bugs 116:"
bug = session.query(Bugs).filter(Bugs.bug_id==116).one()
show_bug(bug)
