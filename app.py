import json

from flask import Flask, render_template, session, redirect, url_for
from access import login_required, group_required, external_required

from auth.routes import blueprint_auth
from query.route import blueprint_query
from report.routes import blueprint_report
from market.routes import blueprint_market

app = Flask(__name__)
app.secret_key = 'SuperKey'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_market, url_prefix='/market')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_query, url_prefix='/query')

app.config['db_config'] = json.load(open('configs/db.json'))
app.config['access_config'] = json.load(open('configs/access.json'))
app.config['cache_config'] = json.load(open('configs/cache.json'))


@app.route('/')
def menu_choice():
    group = session.get('user_group', None)

    if group and group != 'external':
        access_list = app.config['access_config'].get(session.get('user_group'), [])
        return render_template('internal_user_menu.html',
                               title='Меню внутреннего пользователя',
                               is_logged=session.get('user_group', None),
                               access_list=access_list)
    else:
        return redirect('/market')


@app.route('/exit')
def exit_func():
    session.clear()
    return render_template('exit.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
