from pathlib import Path

from flask import Flask, request, abort, g

from .config_ops import load_base_dir, ConfigExtension

config_extension = ConfigExtension()

app = Flask(__name__)
config_extension.init_app(app)

@app.route('/api/show_file_content')
def show_file_content():
    file_name = request.args.get('filename')
    filter_str = request.args.get('filter')
    as_html = request.args.get('ashtml')

    if not file_name:
        abort(400)

    try:
        base_path = Path(g.base_dir).resolve()
        file_path = (base_path / Path(file_name)).resolve()
    except OSError: # resolve may throw error if path have reserved symbols
        abort(403)

    if not file_path.is_relative_to(base_path) or not file_path.is_file():
        abort(403)

    with open(file_path) as f:
        data = f.readlines()
        if filter_str:
            data = get_filtered_data(data, filter_str)

        return get_formatted(data, as_html)

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