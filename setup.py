#!/usr/bin/env python
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def run_setup():
    setup(
        name='declare-amqp',
        version='0.0.5',
        description='A way to declare your AMQP exchanges, queues, and bindings outside of the application',
        keywords = 'amqp',
        url='http://github.com/philipcristiano/declare-amqp',
        author='Philip Cristiano',
        author_email='philipcristiano@gmail.com',
        license='BSD',
        packages=['declareamqp'],
        install_requires=[
            'pika',
            'pyyaml',
        ],
        test_suite='tests',
        long_description=read('README.md'),
        zip_safe=True,
        classifiers=[
        ],
        entry_points="""
        [console_scripts]
            declare-amqp=declareamqp.damqp:main
        """,
    )

if __name__ == '__main__':
    run_setup()
