from setuptools import setup, find_packages
from version import version

setup(
    name='subhajit_engg_tools',
    version=version,
    author='Subhajit Maji',
    author_email='subhajitsr@gmail.com',
    description='Useful data engineering tools',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/subhajitsr/subhajit-engineering-tools',
    project_urls={
        'Bug Tracker': 'https://github.com/subhajitsr/subhajit-engineering-tools',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=find_packages(),
    python_requires='>=3.6',
)
