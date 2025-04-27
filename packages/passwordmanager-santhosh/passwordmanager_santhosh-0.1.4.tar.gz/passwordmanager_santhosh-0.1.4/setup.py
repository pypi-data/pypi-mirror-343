from setuptools import setup, find_packages

setup(
    name='passwordmanager-santhosh',  # your package name (must be unique on PyPI)
    version='0.1.4',
    author='Santhosh Andavar',
    author_email='your_email@example.com',  # (replace with your email)
    description='A simple CLI Password Manager with master password, password strength check, and rotation warning.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/santhoshandavar10/PasswordManager',
    packages=find_packages(),
    install_requires=[
        # List your project dependencies here (from requirements.txt)
    ],
    entry_points={
        'console_scripts': [
            'passwordmanager=passwordmanager.main:main',  # format: command_name=module:function
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # or whatever license you choose
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
