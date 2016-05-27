#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import random
import subprocess

import bottle
from bottle import request, template, static_file

from predictor import Predictor


app = bottle.Bottle()

WORK_DIR = os.path.join(os.getcwd(), 'work_files')
os.makedirs(WORK_DIR, exist_ok=True)

@app.route('/')
@app.post('/')
def index():
    learnfile = request.files.get('learnfile')
    testfile = request.files.get('testfile')
    if learnfile is None or testfile is None:
        return template('index.html', status='Загрузите файлы', results=[])

    name_learnfile, ext_learnfile = os.path.splitext(learnfile.filename)
    name_testfile, ext_testfile = os.path.splitext(testfile.filename)
    if ext_learnfile not in ('.zip',) or ext_testfile not in ('.zip',):
        return template('index.html', status='Не то расширение файла. Нужен zip', results=[])

    current_id = next(id_gen())
    learn_zip = os.path.join(WORK_DIR, 'learn-{0}.zip'.format(current_id))
    test_zip = os.path.join(WORK_DIR, 'test-{0}.zip'.format(current_id))
    learn_dir = os.path.join(WORK_DIR, 'learn-{0}'.format(current_id))
    test_dir = os.path.join(WORK_DIR, 'test-{0}'.format(current_id))
    learnfile.save(learn_zip)
    testfile.save(test_zip)

    unzip_status_learn = unzip_file(learn_zip, learn_dir)
    unzip_status_test = unzip_file(test_zip, test_dir)

    if not os.path.exists(learn_dir)  or not os.path.exists(test_dir):
        return template('index.html', status='Ошибка распаковки', results=[])

    predictor = Predictor(learn_dir, test_dir)
    accuracy, results = predictor.estimate()
    return template('index.html', status='Держи ответ:', accuracy= accuracy, results=results)

def unzip_file(filename, dest_dir):
    bash_command = 'unzip {0} -d {1}'.format(filename, dest_dir)
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    return  output


def id_gen():
    char_set = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    while True:
        new_id = ''.join(random.sample(char_set * 5, 5))
        yield new_id

# Routes for static files
@app.get(r'/<filename:re:.*\.(js|css)>')
def javascripts(filename):
    filename = filename.rpartition('/')[2]
    return static_file(filename, root='static')


@app.get(r'/<filename:re:.*\.ico>')
def stylesheets(filename):
    filename = filename.rpartition('/')[2]
    return static_file(filename, root='static')


@app.get(r'/<filename:re:.*\.(png|jpg)>')
def images(filename):
    filename = filename.rpartition('/')[2]
    return static_file(filename, root='static')


@app.error(404)
def error404(error):
    return '<h1>404</h1><br/>' + error


bottle.run(app, host='localhost', port=8001, reloader=True)
