from setuptools import setup

setup(
    name='giacore',
    version='0.1.0',
    py_modules=['giacore'],
    entry_points='''
        [console_scripts]
        giacore=giacore:giacore
    ''',
)
