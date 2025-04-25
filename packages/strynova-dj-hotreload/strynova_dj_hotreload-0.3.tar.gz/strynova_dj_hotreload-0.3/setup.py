from setuptools import setup, find_packages

setup(
    name="strynova_dj_hotreload",
    version="0.3",
    packages=find_packages(),
    install_requires=[
        "django>=5.1.8",
        "websockets>=10.0",
    ],
    author="Derek Bantel",
    author_email="derekbantel@outlook.com",
    description="Add hot reloading to Django apps.",
    keywords="django, hotreload, strynova",
    url="https://github.com/strynova/strynova-dj-hotreload",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    include_package_data=True,
)
