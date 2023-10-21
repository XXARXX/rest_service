import argparse

from server import app
from config_ops import make_config

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True, dest='subcommand')

    server_parser = subparsers.add_parser('server', help='server subcommands')
    server_parser.add_argument('-ip', '--address', default='127.0.0.1', help='bind address')
    server_parser.add_argument('-p', '--port', default=5000, help='port')

    config_parser = subparsers.add_parser('config', help='config subcommands')
    config_parser.add_argument('-b', '--base-dir', required=True, dest='base_dir', help='base directory where search files')
    
    args = vars(parser.parse_args())
    if args['subcommand'] == 'server':
        ip = args['address']
        port = args['port']

        app.run(host=ip, port=port, debug=True)
    elif args['subcommand'] == 'config':
        make_config(args)

if __name__ == '__main__':
    main()