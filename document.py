import os

from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(255))
    content = Column(Text)
    group = Column(String(255))

def get_engine():
    username = 'clarify'
    password = 'clarifypassword123'
    port = 5432
    database = 'clarify'
    return create_engine('postgresql://{}:{}@{}:{}/{}'.format(username, password, os.getenv('DB_HOST'), port, database))

def create_session() -> Session:
    engine = get_engine()
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()

def get_user_by_name(session, name):
    return session.query(User).filter(User.name == name).first()

def get_documents_by_user(session, user):
    return session.query(Document).filter(Document.user_id == user.id).all()

def get_document_by_id(session, document_id):
    return session.query(Document).filter(Document.id == document_id).first()

def create_user(session, name):
    user = User(name=name)
    session.add(user)
    session.commit()
    return user

def create_document(session, user, title, content, group):
    document = Document(user_id=user.id, title=title, content=content, group=group)
    session.add(document)
    session.commit()
    return document

def update_document(session, document, title, content, group):
    document.title = title
    document.content = content
    document.group = group
    session.commit()
    return document

def delete_document(session, document):
    session.delete(document)
    session.commit()
