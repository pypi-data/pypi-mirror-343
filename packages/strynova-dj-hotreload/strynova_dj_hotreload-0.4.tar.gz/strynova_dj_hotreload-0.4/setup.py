import os
from setuptools import setup, find_packages

# Read the contents of README.md
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8') as readme:
    README = readme.read()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="strynova_dj_hotreload",
    version="0.4",
    packages=find_packages(),
    author="Derek Bantel",
    author_email="derekbantel@outlook.com",
    description="Add hot reloading to Django apps.",
    long_description=README,
    long_description_content_type='text/markdown',
    keywords="django, hotreload, strynova",
    url="https://github.com/strynova/strynova-dj-hotreload",
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=3.2',
        "websockets>=10.0",
    ],
    include_package_data=True,
)
