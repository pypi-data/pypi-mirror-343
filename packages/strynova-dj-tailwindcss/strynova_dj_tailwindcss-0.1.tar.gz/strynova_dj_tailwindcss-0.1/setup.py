import os
from setuptools import setup, find_packages

# Read the contents of README.md
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8') as readme:
    README = readme.read()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='strynova-dj-tailwindcss',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A Django package for integrating Tailwind CSS',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/strynova/strynova_dj_tailwindcss',
    author='Derek Bantel',
    author_email='derekbantel@outlook.com',
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
        'tailwindcss',
        'tailwindcss-cli',
    ],
    python_requires='>=3.7',
    keywords='django, tailwind, css, tailwindcss, frontend',
)
