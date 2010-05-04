from setuptools import setup, find_packages

setup(
    name = "socialinis-tinklas",
    version = "1.0",
    url = "http://github.com/gytis/Projektas",
    description = "Socialinis tinklas",
    author = 'Gytis Trikleris',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
    
)