# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField
from flask_login import current_user
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import User, Preference


class RegisterForm(FlaskForm):
    """Register form."""

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify password',
                            [DataRequired(), EqualTo('password', message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('Username already registered')
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append('Email already registered')
            return False
        return True

class PreferencesForm(FlaskForm):
    """Preferences Form."""

    class_field = SelectField('Class', choices=[('61a', 'CS 61A'), ('61b', 'CS 61B'), ('70', 'CS 70')])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(PreferencesForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(PreferencesForm, self).validate()
        if not initial_validation:
            return False
        pref = Preference.query.filter_by(user_id=current_user.id, class_field=self.class_field.data).first()
        if pref:
            self.class_field.errors.append('Already submitted this preference.')
            return False
        return True
