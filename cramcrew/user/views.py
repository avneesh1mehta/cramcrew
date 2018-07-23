# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import not_, or_, and_

from cramcrew.user.models import User, Preference
from cramcrew.user.forms import PreferencesForm
from cramcrew.utils import flash_errors

blueprint = Blueprint('user', __name__, url_prefix='/user', static_folder='../static')


@blueprint.route('/preferences')
@login_required
def preferences():
    """List members."""
    my_prefs = Preference.query.filter_by(user_id=current_user.id)
    classes = []
    for pref in my_prefs:
        assert type(pref.class_field) == str
        classes.append(pref.class_field)
    overlapping = Preference.query.filter(and_(not_(Preference.user_id==current_user.id), Preference.class_field.in_(classes)))
    return render_template('users/preferences.html', prefs=overlapping)

@blueprint.route('/find', methods=['GET', 'POST'])
@login_required
def find():
    form = PreferencesForm(request.form)
    if form.validate_on_submit():
        assert(current_user != None)
        Preference.create(class_field=form.class_field.data, user=current_user)
        flash('Thank you for submitting a preference.', 'success')
        return redirect(url_for('user.preferences'))
    else:
        flash_errors(form)
    return render_template('users/find.html', form=form)
