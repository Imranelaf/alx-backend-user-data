#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base


from user import Base, User


class DB:
    '''
    This class is the database interface
    Methods:
        add_user: add a new user to the db
        find_user_by: find a user from the db given arbitrary args
        update_user: update a user in the db with arbitrary args
    '''

    def __init__(self) -> None:
        '''
        Constructor
        '''
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        '''
        This function should return the current session
        Returns:
            Session: the current session
        '''
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''
        This function should add a user to the database
        Args:
            email: string type
            hashed_password: string type
        Returns:
            User: a new user object
        '''
        usr = User(email=email, hashed_password=hashed_password)
        self._session.add(usr)
        self._session.commit()
        return usr

    def find_user_by(self, **kwargs) -> User:
        '''
        This function should find a user in the database
        Args:
            **kwargs: arbitrary keyword arguments
        Returns:
            User: a user object
        '''
        try:
            usr = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()
        return usr

    def update_user(self, user_id: int, **kwargs) -> None:
        '''
        This function should update a user in the database
        Args:
            user_id: integer type
            **kwargs: arbitrary keyword arguments
        Returns:
            None
        '''
        usr = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if hasattr(usr, key):
                setattr(usr, key, value)
            else:
                raise ValueError
        self._session.commit()
