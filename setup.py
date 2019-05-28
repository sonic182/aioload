"""Setup module."""

from setuptools import setup
try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements


def requirements(filename):
    """Parse requirements from requirements.txt."""
    reqs = parse_requirements(filename, session=False)
    return [str(req.req) for req in reqs]


setup(
    name='load_test',
    version='0.0.1',
    description='Load test tool',
    author='Johanderson Mogollon',
    author_email='johanderson@doofinder.com',
    license='MIT',
    packages=['load_test'],
    setup_requires=['pytest-runner'],
    test_requires=['pytest'],
    install_requires=requirements('requirements.txt'),
    extras_require={
        'dev': requirements('dev-requirements.txt'),
        'test': [
            'pytest',
            'pytest-cov',
            'pytest-sugar',
            'coverage',
            'coveralls'
        ]
    }
)
