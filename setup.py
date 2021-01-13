import setuptools

requires = [
    'requests==2.25.0',
    'rdflib==5.0.0',
    'minio==6.0.0',
    'ipython==7.16.1',
    'prefect==0.14.1',
]

setuptools.setup(
    name='giacore',
    version='0.1.0',
    py_modules=setuptools.find_packages(),
    install_requires=requires,
    entry_points='''
        [console_scripts]
        giacore=giacore:giacore
    ''',
)
