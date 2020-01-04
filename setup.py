from setuptools import setup, find_packages

setup(
    name='djomotic',
    version='1.0.0.dev0',
    url='https://github.com/gutard/djomotic',
    author='Gaël Utard',
    author_email='gael.utard@laposte.net',
    description='Domotic with Django',
    packages=find_packages(),    
    install_requires=[
        'django',
        'pyserial',
    ],
)
