"""Setup module."""

from setuptools import setup


def read_file(filename):
    """Read file correctly."""
    with open(filename) as _file:
        return _file.read().strip()


setup(
    name='aioload',
    version=read_file('VERSION'),
    description='Load test tool',
    long_description=read_file('README.rst'),
    author='Johanderson Mogollon',
    author_email='johanderson@mogollon.com.ve',
    url='https://github.com/sonic182/aioload',
    license='MIT',
    packages=['aioload'],
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
    install_requires=[
        'aiohttp',
        'cchardet',
        'aiodns',
        'matplotlib',
        'pandas'
    ],
    # other arguments here...
    entry_points={
        'console_scripts': [
            'aioload=aioload:main',
        ]
    },
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
            'pytest-asyncio',
            'coveralls',
            'pytest-flake8',
        ]
    }
)
