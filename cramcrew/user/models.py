# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin, current_user

from cramcrew.database import Column, Model, SurrogatePK, db, reference_col, relationship
from cramcrew.extensions import bcrypt


class Preference(SurrogatePK, Model):
    """A class preference for a user."""

    __tablename__ = 'preferences'
    class_field = Column(db.String(80), unique=False, nullable=False)
    user_id = reference_col('user', nullable=True)

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
