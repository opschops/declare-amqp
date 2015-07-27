from argparse import ArgumentParser
import os
import sys
import pika
import yaml


def run(args):
    host = os.getenv('AMQP_HOST', 'localhost')
    user = os.getenv('AMQP_USER', 'guest')
    password = os.getenv('AMQP_PASS', 'guest')
    vhost = os.getenv('AMQP_VHOST', '/')

    credentials = pika.PlainCredentials(user, password)
    parameters = pika.ConnectionParameters(
      credentials=credentials,
      virtual_host=vhost, host=host)

    config = get_config(args.config)

    connection = pika.BlockingConnection(parameters)
    ch = connection.channel()

    for exchange in config.get('exchanges'):
        print 'Declaring exchange:'
        print '\t', exchange
        try:
            ch.exchange_declare(
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
            ch.queue_declare(
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

                if binding.get('binding_key'):
                    ch.queue_bind(
                        queue['name'],
                        binding['exchange'],
                        binding['binding_key'],
                    )
                else:
                    ch.queue_bind(
                        queue['name'],
                        binding['exchange']
                    )
            except AttributeError as ae:
                print ae
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