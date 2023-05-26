from setuptools import setup, find_packages

setup(
    name='kivy_mobile',
    version='1.1.7',
    author='ReactBoysTeam',
    author_email='selik.04dn@gmail.com',
    setup_requires=['flake8'],
    packages=find_packages(include=['kivy_mobile_app', 'kivy_mobile_app.*']),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'kivy>=1.9.1',
        'kivymd'
        ]
)