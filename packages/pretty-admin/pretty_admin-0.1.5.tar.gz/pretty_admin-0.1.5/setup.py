from setuptools import setup, find_packages
import os

# Get absolute path of this file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, '../README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pretty_admin',
    version='0.1.5',
    packages=find_packages(),
    include_package_data=True,
    description='A Tailwind-based Django admin UI skin',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Pruthviraj Chokake',
    author_email='chokake.pruthvi@gmail.com',
    license='MIT',
    url='https://github.com/Pruthvi2121/pretty_admin',  
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'Django>=3.2',
        'setuptools'
    ],
    python_requires='>=3.6',
    project_urls={
        'Homepage': 'https://github.com/Pruthvi2121/pretty_admin',  
        'Bug Tracker': 'https://github.com/Pruthvi2121/pretty_admin/issues',
    },
)
