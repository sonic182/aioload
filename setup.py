"""Setup module."""

from setuptools import setup


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
    install_requires=[
        'aiohttp',
        'cchardet',
        'aiodns',
        'pandas'
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
            'pytest-asyncio',
            'pytest-flake8',
        ]
    }
)
