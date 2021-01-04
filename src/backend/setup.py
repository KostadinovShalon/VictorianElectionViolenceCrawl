from setuptools import find_packages, setup

setup(
    name='vev_crawler',
    version='2.1.0',
    python_requires='>=3',
    author='Brian K Isaac Medina',
    url='https://github.com/KostadinovShalon/VictorianElectionViolenceCrawl',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "beautifulsoup4~=4.9.3",
        "paramiko~=2.7.2",
        "Pillow~=8.0.1",
        "python-dateutil~=2.8.1",
        "requests~=2.25.1",
        "scrapy~=2.4.1",
        "SQLAlchemy~=1.3.22",
        "w3lib~=1.22.0",
        "crochet~=1.12.0",
        "Flask~=1.1.2",
        "PyYAML~=5.3.1",
        "pandas~=1.2.0",
        "numpy~=1.19.4",
        "mysqlclient~=2.0.3"
        "wheel",
        "waitress",
        "flask-cors"
    ],
)
