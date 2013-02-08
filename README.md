# Declare AMQP

A way to declare your exchanges, queues, and bindings outside of the application

## Installing

    pip install declare-amqp

## Declaration

You can see the extend of configuration in the `example_config.yml` file. All
fields used are currently required except for the `arguments` on exchanges.

    exchanges:
      - name: example_exchange
        type: direct
        durable: True
        auto_delete: False
        arguments:
          alternate-exchange: your_alternate_exchange

    queues:
      - name: test_queue
        auto_delete: False
        durable: True
        bindings:
          - exchange: example_exchange
            binding_key: test_binding

When I have the need for them exchange-to-exchange bindings will be added.

## Running

### ENVVARS

    AMQP_HOST (default: localhost)

    AMQP_USER (default: guest)

    AMQP_PASS (default: guest)

    AMQP_VHOST(default: /)


### CLI

Once you have set the envvars you are set to run `declare-amqp`

    declare-amqp --config your_config.yml
