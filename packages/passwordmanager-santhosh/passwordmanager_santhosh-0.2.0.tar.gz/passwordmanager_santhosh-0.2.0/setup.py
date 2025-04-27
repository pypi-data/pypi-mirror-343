from setuptools import setup, find_packages

setup(
    name='passwordmanager-santhosh',
    version='0.2.0',
    author='Santhosh Andavar',
    author_email='your_email@example.com',
    description='A simple CLI Password Manager',
    packages=find_packages(),
    install_requires=['colorama'],
    entry_points={
        'console_scripts': [
            'passwordmanager=passwordmanager.cli:main'
        ]
    },
    python_requires='>=3.6',
)
