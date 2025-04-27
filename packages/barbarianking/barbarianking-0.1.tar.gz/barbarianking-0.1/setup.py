from setuptools import setup, find_packages

setup(
    name='barbarianking',   # package name
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'barbarian = my_package.mycode:main',  # command = file:function
        ],
    },
)
