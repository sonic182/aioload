"""Setup module."""

from setuptools import setup


setup(
    name='aioload',
    version='0.0.1',
    description='Load test tool',
    author='Johanderson Mogollon',
    author_email='johanderson@mogollon.com.ve',
    license='MIT',
    packages=['aioload'],
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
