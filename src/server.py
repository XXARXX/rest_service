from pathlib import Path

from flask import Flask, request, abort, g

from .config import load_base_dir
from .config_ext import ConfigExtension

config_extension = ConfigExtension()

def create_app(test_env: bool = False):
    app = Flask(__name__)
    config_extension.init_app(app)

    @app.route('/api/show_file_content')
    def show_file_content():
        file_name = request.args.get('filename')
        filter_str = request.args.get('filter')
        as_html = request.args.get('ashtml')

        if filter_str is not None:
            if not validate_filter(filter_str):
                abort(400)

            filter_str = filter_str[1:-1]

        if not file_name:
            abort(400)

        try:
            base_path = Path(g.base_dir).resolve()
            file_path = (base_path / Path(file_name)).resolve()
        except OSError: # resolve may throw error if path have reserved symbols
            abort(403)

        if not file_path.is_relative_to(base_path) or not file_path.is_file():
            abort(404)

        with open(file_path) as f:
            data = f.readlines()
            if filter_str:
                data = get_filtered_data(data, filter_str)

            return get_formatted(data, as_html)

    return app

def validate_filter(filter_str):
    if len(filter_str) < 2:
        return False
    if not (filter_str.startswith('"') and filter_str.endswith('"')):
        return False
    
    return True

def get_formatted(data: list, as_html: any):
    if as_html:
        return get_html_formatted(data)
    else:
        return get_raw_str(data)

def get_html_formatted(data: list):
    result = ''
    for line in data:
        result += '<p>{0}</p>'.format(line)
    return result

def get_raw_str(data: list):
    result = ''
    for line in data:
        result += line
    return result

def get_filtered_data(data: list, filter_str):
    return list(filter(filter_func(filter_str), data))

def filter_func(substring):
    def with_filter(entry):
        if substring in entry:
            return True
        return False

    return with_filter