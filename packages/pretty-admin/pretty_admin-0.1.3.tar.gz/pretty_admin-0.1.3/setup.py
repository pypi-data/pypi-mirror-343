from setuptools import setup, find_packages

setup(
    name='pretty_admin',
    version='0.1.3',
    packages=find_packages(),
    include_package_data=True,
    description='A Tailwind-based Django admin UI skin',
    author='Pruthviraj Chokake',
    install_requires=[
        'Django>=3.2',
        'setuptools'
    ],
)
