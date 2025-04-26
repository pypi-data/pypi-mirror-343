from setuptools import setup, find_packages

setup(
    name='dot_cmd_parser',  # Module name
    version='0.1.0',          # Version number
    packages=find_packages(),  # Automatically discover all packages
    description='A parser for dot-separated commands with argument handling and error correction.',
    long_description=open('README.md').read(),  # Load long description from README.md
    long_description_content_type='text/markdown',
    author='Shriram Bhogale',  # Replace with your name
    author_email='bhogaleshriram555@gmail.com',  # Replace with your email
    url='https://github.com/bhogaleShriram/DotCommandParser',  # Replace with your project URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Replace with the license you choose
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify minimum Python version
)
