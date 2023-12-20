import json
import os

from flask import (
    Blueprint, render_template,
    request, current_app,
    session, redirect, url_for
)

from access import group_required
from cache.wrapper import fetch_from_cache
from database.operations import select, call_procedure
from database.sql_provider import SQLProvider

blueprint_report = Blueprint(
    'blueprint_report',
    __name__,
    template_folder='templates',
    static_folder='static'
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/', methods=['GET'])
@group_required
def index():
    db_config = current_app.config['db_config']
    cache_config = current_app.config['cache_config']
    cached_func = fetch_from_cache('all_reports', cache_config)(select)

    sql = provider.get('get_all_reports.sql')
    result = cached_func(db_config, sql)

    session['reports'] = {row['proc_name']: json.loads(row['data']) for row in result}
    access_list = current_app.config['access_config'].get(session.get('user_group'), [])

    return render_template('report/index.html',
                           reports=session['reports'],
                           access_list=access_list)


@blueprint_report.route('/<report_id>/create', methods=['GET', 'POST'])
@group_required
def report_create(report_id):
    if not (session.get('reports', None) and session['reports'].get(report_id, None)):
        return redirect(url_for('blueprint_report.index'))

    db_config = current_app.config['db_config']

    if request.method == 'GET':
        parameters = session['reports'][report_id]['parameters']

        return render_template('report/input_form.html',
                               title='Создание отчета',
                               report_id=report_id,
                               parameters=parameters)
    else:
        parameters = session['reports'][report_id]['parameters']
        form = {key: request.form.get(key, None) for key in parameters.keys()}
        table = session['reports'][report_id]['table']
        sql = provider.get(table + '.sql', **form)
        result = select(db_config, sql)

        print(result)

        if result:
            return render_template('report/input_form.html',
                                   title='Создание отчета',
                                   report_id=report_id, parameters=parameters,
                                   error='Отчет уже существует')

        args = list(form.values())
        result = call_procedure(db_config, report_id, *args)

        if not result:
            return render_template('report/input_form.html',
                                   title='Создание отчета',
                                   report_id=report_id, parameters=parameters,
                                   error='Отчет не может быть создан')

        table = session['reports'][report_id]['table']
        sql = provider.get(table + '.sql', **form)
        result = select(db_config, sql)

        return render_template('report/dynamic.html',
                               name=session['reports'][report_id]['name'],
                               report_id=report_id, table_items=result,
                               back_site=request.endpoint)


@blueprint_report.route('/<report_id>/view', methods=['GET', 'POST'])
@group_required
def report_view(report_id):
    if not (session.get('reports', None) and session['reports'].get(report_id, None)):
        return redirect(url_for('blueprint_report.index'))

    db_config = current_app.config['db_config']

    if request.method == 'GET':
        parameters = session['reports'][report_id]['parameters']

        return render_template('report/input_form.html',
                               title='Просмотр отчета',
                               report_id=report_id,
                               parameters=parameters)
    else:
        parameters = session['reports'][report_id]['parameters']
        form = {key: request.form.get(key, None) for key in parameters.keys()}

        table = session['reports'][report_id]['table']
        sql = provider.get(table + '.sql', **form)
        result = select(db_config, sql)

        if not result:
            return render_template('report/input_form.html',
                                   report_id=report_id, parameters=parameters,
                                   error='Отчета с заданными параметрами не существует')

        return render_template('report/dynamic.html',
                               name=session['reports'][report_id]['name'],
                               report_id=report_id, table_items=result,
                               back_site=request.endpoint)
