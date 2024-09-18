from setuptools import setup

setup(
    name='subhajit_engg_tools',
    version='0.0.6',
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
    packages=['subhajit_engg_tools'],  # Adjust if you have multiple packages or submodules
    python_requires='>=3.6',
)
