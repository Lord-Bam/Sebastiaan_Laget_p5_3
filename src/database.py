from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class Database:
    _instance = None
    Base = declarative_base()

    def __new__(cls, config=None):
        if cls._instance is None:
            if config is None:
                raise ValueError("A configuration must be provided for the first instantiation.")
            cls._instance = super().__new__(cls)
            cls._instance._initialize(config)
        return cls._instance

    def _initialize(self, config):
        self.engine = create_engine(config['DB']["database_uri"])
        self.Session = sessionmaker(bind=self.engine)
        self.Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()

    def drop_all(self):
        self.Base.metadata.drop_all(self.engine)

    def create_all(self):
        self.Base.metadata.create_all(self.engine)
