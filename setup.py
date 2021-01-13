import setuptools

setuptools.setup(
    name='giacore',
    version='0.1.0',
    py_modules=setuptools.find_packages(),
    entry_points='''
        [console_scripts]
        giacore=giacore:giacore
    ''',
)
