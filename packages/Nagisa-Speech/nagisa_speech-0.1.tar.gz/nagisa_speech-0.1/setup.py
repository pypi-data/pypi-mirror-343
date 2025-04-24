from setuptools import setup, find_packages

setup(
    name='Nagisa_Speech',
    version='0.1',
    author='Manvendra Singh ',
    author_email='techno99933@gmail.com',
    description='This is the official Nagisa SpeechToText package created by Manvendra Singh',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'webdriver_manager'
    ]
)

