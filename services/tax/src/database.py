from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session



SQLALCHEMY_DATABASE_URL = "postgresql://user:pass@db:5432/tax"
 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)