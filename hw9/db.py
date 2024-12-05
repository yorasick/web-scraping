from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String)
    external_id = Column(String)
    title = Column(String)
    url = Column(String)
    price = Column(Float)
    old_price = Column(Float)


class DatabaseManager:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.engine = None
        self.session = None


    def connect(self) -> None:
        self.engine = create_engine(self.connection_string)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


    def close(self) -> None:
        if self.session:
            self.session.close()


    def insert_products(self, data: list[dict]) -> None:
        if not self.session:
            raise RuntimeError("Database connection not established. Call connect() first.")
        
        for product in data:
            self.session.merge(Product(**product), load=True)
        
        self.session.commit()