
[![Build Status](https://travis-ci.org/sonic182/load_test_aiohttp.svg?branch=master)](https://travis-ci.org/sonic182/load_test_aiohttp)
[![Coverage Status](https://coveralls.io/repos/github/sonic182/load_test_aiohttp/badge.svg?branch=master)](https://coveralls.io/github/sonic182/load_test_aiohttp?branch=master)

# load test

load test tool using aiohttp, cchardet and aiodns. for drawing charts we use matplotlib and pandas.

# Requirements

* Python>=3.5.3
* install requirements by installing package `pip install -e .` (-e for editable installation) or installing requirements.txt


# Usage

```bash

# python run.py --help
usage: run.py [-h] [-s SETTINGS] [-d] [-v] [-n NUMBER_OF_REQUESTS]
              [-c CONCURRENCY] [--plot]

optional arguments:
  -h, --help            show this help message and exit
  -s SETTINGS, --settings SETTINGS
  -d, --debug
  -v, --verbose
  -n NUMBER_OF_REQUESTS, --number_of_requests NUMBER_OF_REQUESTS
  -c CONCURRENCY, --concurrency CONCURRENCY
  --plot                draw charts if present
# python run.py -n 3000 -c 50 --plot -v
2019-05-29 11:02:32,758 - __init__:113 - INFO - 2748a248ebe143fead3ed58396df4fda - Starting script... -
2019-05-29 11:02:37,027 - __init__:88 - INFO - 2748a248ebe143fead3ed58396df4fda - done - min=15.725; max=129.479; mean=67.37412766666667; stdev=13.231390347536328; codes.200=3000; concurrency=50; requests=3000;
```

# Contribute

1. Fork
2. create a branch `feature/your_feature`
3. commit - push - pull request

Thanks :)
