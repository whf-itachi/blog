from datetime import datetime
from flask import redirect, render_template, session, url_for
from . import main
# from .forms import NameForm
from .. import db
from ..models import User


def index():
    '''form = NameForm()
    if form.validate_on_submit():
        # ...
        return redirect(url_for('.index'))'''
    return render_template('index.html', form='form', name=session.get('name'),
                           known=session.get('known', False),
                           current_time=datetime.utcnow())
