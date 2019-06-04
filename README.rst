|build status| |coverage status|

aioload
=========

Load test tool using aiohttp, cchardet and aiodns. for drawing charts we
use matplotlib and pandas.

Requirements
============

-  python>=3.5.3
-  install requirements by installing package ``pip install -e .`` (-e
   for editable installation) or installing requirements.txt

Installation
============

.. code:: bash

  pip install aioload

Usage
=====

you need to specify your request in a settings file like **config.ini**

.. code:: ini

   [http]
   sock_read = 30
   sock_connect = 3


   [test]
   # target url for test
   url = http://localhost:8080/api/v1/something
   # methods: get, post, put, delete
   method = post
   #
   # use body for send body in request
   # if body is json, indicate correct header in headers section
   body = '{"foo": "bar"}'

   # query params if needed, this will transform url
   # in something like http://localhost:8080/api/v1/something?token=something
   [params]
   token = something

   # headers if needed
   [headers]
   content-type = application/json

usage example

.. code:: bash

   > aioload -h
   usage: aioload [-h] [-d] [-v] [-n NUMBER_OF_REQUESTS] [-c CONCURRENCY]
                  [--plot]
                  testfile
   
   positional arguments:
     testfile              Test file to be executed
   
   optional arguments:
     -h, --help            show this help message and exit
     -d, --debug           true if present
     -v, --verbose         true if present
     -n NUMBER_OF_REQUESTS, --number_of_requests NUMBER_OF_REQUESTS
                           number of requests to be done, default: 100
     -c CONCURRENCY, --concurrency CONCURRENCY
                           concurrency (requests at the same time), default: 10
     --plot                draw charts if present

   > aioload config.ini -n 3000 -c 100 --plot -v
   2019-05-29 17:20:51,662 - __init__:135 - info - 8cf56ded860f41d8a86dab2aed05218f - starting script... -
   2019-05-29 17:20:55,301 - __init__:102 - info - 8cf56ded860f41d8a86dab2aed05218f - done - min=14.54ms; max=212.21ms; mean=109.36ms; req/s=600.0; req/q_std=333.7; stdev=24.65; codes.200=3000; concurrency=100; requests=3000;

.. figure:: ./charts.jpg
   :alt: preview1

   preview1

Contribute
==========

1. fork
2. create a branch ``feature/your_feature``
3. commit - push - pull request

thanks :)

.. |build status| image:: https://travis-ci.org/sonic182/load_test_aiohttp.svg?branch=master
   :target: https://travis-ci.org/sonic182/load_test_aiohttp
.. |coverage status| image:: https://coveralls.io/repos/github/sonic182/load_test_aiohttp/badge.svg?branch=master
   :target: https://coveralls.io/github/sonic182/load_test_aiohttp?branch=master
