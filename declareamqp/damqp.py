from argparse import ArgumentParser
import os
import sys

from haigha.connections.rabbit_connection import RabbitConnection
from haigha.message import Message
import yaml


def run(args):
    host = os.getenv('AMQP_HOST', 'localhost')
    user = os.getenv('AMQP_USER', 'guest')
    password = os.getenv('AMQP_PASS', 'guest')
    vhost = os.getenv('AMQP_VHOST', '/')

    connection = RabbitConnection(
      user=user, password=password,
      vhost=vhost, host=host,
      heartbeat=None, debug=True)

    config = get_config(args.config)

    ch = connection.channel()
    for exchange in config.get('exchanges'):
        print 'Declaring exchange:'
        print '\t', exchange
        try:
            ch.exchange.declare(
                exchange['name'],
                exchange['type'],
                durable=exchange['durable'],
                auto_delete=exchange['auto_delete'],
                arguments=exchange.get('arguments', {}),
            )
        except AttributeError as ae:
            print ae
            print 'Declare conflict! This must be fixed manually'
            sys.exit(1)

    for queue in config.get('queues'):
        print 'Declaring queue:'
        print '\t', queue
        try:
            ch.queue.declare(
                queue['name'],
                auto_delete=queue['auto_delete'],
                durable=queue['durable'],
                arguments=queue.get('arguments', {}),
            )
        except AttributeError as ae:
            print ae
            print 'Declare conflict! This must be fixed manually'
            sys.exit(1)
        for binding in queue['bindings']:
            print 'Binding queue:'
            print '\t', binding
            try:
                ch.queue.bind(
                    queue['name'],
                    binding['exchange'],
                    binding['binding_key'],
                )
            except AttributeError:
                print 'Declare conflict! This must be fixed manually'
                sys.exit(1)
    connection.close()


def get_args():
    parser = ArgumentParser(description='Declare some AMQP')
    parser.add_argument('--config', metavar='config', type=str, help='Config file to use')

    return parser.parse_args()

def get_config(path):
    print path
    config_file = open(path)
    content = config_file.read()
    config_file.close()
    return yaml.load(content)

def main():
    run(get_args())

if __name__ == '__main__':
    main()
