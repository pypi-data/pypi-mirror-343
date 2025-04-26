from setuptools import setup, find_packages

setup(
    name='tugaspypi',
    version='0.1.0',
    author='Afif Ramadhani',
    author_email='Lontong@gmail.com',
    description=' Ini Tugas PYPI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.6',
)
