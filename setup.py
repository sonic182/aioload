"""Setup module."""

import re
from setuptools import setup


def read_file(filename):
    """Read file correctly."""
    with open(filename) as _file:
        return _file.read().strip()


def requirements(filename):
    """Parse requirements from file."""
    return re.findall(r'([\w-]+[<=>]{1}=[\d.]+)', read_file(filename)) or []


def override(requirements, overrides):
    """Override requirements.txt"""
    def override_it(item):
        for key in overrides:
            if key in item:
                return overrides[key]
        return item
    return list(map(override_it, requirements))


setup(
    name='aioload',
    version=read_file('VERSION'),
    description='Load test tool',
    long_description=read_file('README.rst'),
    author='Johanderson Mogollon',
    author_email='johanderson@mogollon.com.ve',
    url='https://github.com/sonic182/aioload',
    license='MIT',
    packages=['aioload', 'aioload_utils'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='testing loadtest load',
    setup_requires=['pytest-runner'],
    test_requires=['pytest'],
    install_requires=override(requirements('requirements.txt'), {
        'matplotlib': 'matplotlib<=3.1.1'
    }),
    # other arguments here...
    entry_points={
        'console_scripts': [
            'aioload=aioload:main',
        ]
    },
    extras_require={
        'test': requirements('test-requirements.txt')
    }
)
