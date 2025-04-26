from setuptools import setup

setup(
    name='cfh',
    version='0.1',
    py_modules=['cfh'],
    install_requires=[
        'Click',
        'GitPython',
    ],
    entry_points='''
        [console_scripts]
        cfh=cfh:main
    ''',
)