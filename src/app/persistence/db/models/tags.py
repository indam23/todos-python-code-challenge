from sqlalchemy import Column, String, Integer

from persistence.db.base import Base

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tag = Column(String, nullable=False, unique=True)

    def __init__(self, tag):
        self.tag = tag
    
    def as_dict(self):
        return {"id": self.id, "tag": self.tag}