# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin, current_user

from cramcrew.database import Column, Model, SurrogatePK, db, reference_col, relationship
from cramcrew.extensions import bcrypt


class Preference(SurrogatePK, Model):
    """A class preference for a user."""

    __tablename__ = 'preferences'
    is_student = Column(db.Boolean(), default=True)
    # not sure what 'class_field' is for...should be associated with either a student or group
    class_field = Column(db.String(80), unique=False, nullable=False)
    # can be either associated to a user or group
    associative_id = reference_col('user', nullable=True)
    
    # For example for one category of preferences: 
    small_groups = Column(db.Boolean(), default=True)
    is_extrovert = Column(db.Boolean(), default=True)
    # The below should be changed to INT. Basically is the score for the above two preferences 
    # need to figure out how to measure preferences (true=1 point? false=0 points?)
    score_outgoing = Column(db.Binary(80), default=True)
    
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    # TODO: As mentioned below, people seem to instantiate columns differently. 
    # Online found: Column('datemodified', TIMESTAMP,
    #  server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    # Whereas I just went off what you have done so please check if compatible
    last_modified = Column(db.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    # TODO: please change below to INT, a 1 in this column means admin
    last_updated_by = Column(db.Binary(128), nullable=False)
    # For now should add each individual preference as a column by itself. In the future can split up preferences depending on 
    # the particular `category` each preference falls into

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Preference({class_field})>'.format(class_field=self.class_field)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'user'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.Binary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    # TODO: As mentioned below, people seem to instantiate columns differently. 
    # Online found: Column('datemodified', TIMESTAMP,
    #  server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    # Whereas I just went off what you have done so please check if compatible
    last_modified = Column(db.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    # TODO: please change below to INT, a 1 in this column means admin
    last_updated_by = Column(db.Binary(128), nullable=False)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
    prefs = relationship('Preference', backref='user')

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)
    

class Groups(SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'groups'
    # TODO: front-end task to make sure each group name is unique; endpoint for this
    screen_name = Column(db.String(80), unique=True, nullable=False)
    # TODO: change below to INT, seems like docs for SQLalchemy have another way of making tables like the method to create columns, etc.
    # Not knowledgeable in which way to make tables and how this all works but make sure the standard is set
    users_count = Column(db.Binary(123), nullable=False)
    description = Column(db.String(250), nullable=True)
    
    # can add its metrics here or just reference its own preference row and see all of its scores
    
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    last_modified = Column(db.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    # TODO: please change below to INT, a 1 in this column means admin
    last_updated_by = Column(db.Binary(128), nullable=False)
    
    # ***** 
    # Make methods after finalizing structure, and we start building frontend to see what exact info we will be 
    # inputting to the db and what we need to retrieve.
    # *****
    
# something that the Technical advisor of fintech company told me to keep in mind. Prolly just cuzz fintech 
# requires much more security. Btw I do not know what surrogatepk and model are so check all of the classes' inputs
class Log(SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'groups'
    
    # some sort of general code for each endpoint so can link back to a particular function call
    description = Column(db.String(250), nullable=True) 
    table = Column(db.String(25), nullable=True)
    # can add its metrics here or just reference its own preference row and see all of its scores
    
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    # TODO: please change below to INT, a 1 in this column means admin
    last_updated_by = Column(db.Binary(128), nullable=False)
    
    # ***** 
    # Make methods after finalizing structure, and we start building frontend to see what exact info we will be 
    # inputting to the db and what we need to retrieve.
    # *****
