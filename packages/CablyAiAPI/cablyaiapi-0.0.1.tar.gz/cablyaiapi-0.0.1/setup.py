from setuptools import setup, find_packages

setup(
    name='CablyAiAPI',
    version='0.0.1',
    author='Fixyres',
    description='Tool for easy use CablyAiAPI (https://cablyai.com)',
    author_email='foxy437@outlook.com',
    packages=find_packages(),
    install_requires=[
        'requests'
    ]
)