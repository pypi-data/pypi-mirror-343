from setuptools import setup, find_packages

setup(
    name='djbackup',
    version='2.0.1',
    description='dj_backup is an installable module for Django that is used for backup purposes.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/FZl47/dj_backup',
    author='FZl47',
    author_email='fzl8747@gmail.com',
    package_data={
        'static': ['./dj_backup/static'],
        'templates': ['./dj_backup/templates'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
