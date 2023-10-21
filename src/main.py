import argparse

from waitress import serve

from .server import create_app
from .config import make_config

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True, dest='subcommand')

    server_parser = subparsers.add_parser('server', help='server subcommands')
    server_parser.add_argument('-ip', '--address', default='127.0.0.1', help='bind address')
    server_parser.add_argument('-p', '--port', default=5000, help='port')
    server_parser.add_argument('-d', '--debug', action='store_true', help='debug mode')

    config_parser = subparsers.add_parser('config', help='config subcommands')
    config_parser.add_argument('-b', '--base-dir', required=True, dest='base_dir', help='base directory where search files')
    
    args = vars(parser.parse_args())
    if args['subcommand'] == 'server':
        ip = args['address']
        port = args['port']
        debug = args['debug']

        if debug:
            create_app().run(host=ip, port=port, debug=True)
        else:
            serve(create_app(), host=ip, port=port)
    
    elif args['subcommand'] == 'config':
        make_config(args)

if __name__ == '__main__':
    main()