import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='ml-django-brain',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A Django plugin for AI/ML integration with model registry, API generation, and monitoring',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/sgh370/ml-django-brain',
    author='Saeed Ghanbari',
    author_email='sgh370@yahoo.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='django, machine learning, ml, ai, model registry, api, monitoring',
    python_requires='>=3.8',
    install_requires=[
        'Django>=3.2',
        'djangorestframework>=3.12.0',
        'numpy>=1.19.0',
        'pandas>=1.1.0',
        'scikit-learn>=0.24.0',
        'joblib>=1.0.0',
        'pyyaml>=5.4.0',
        'jsonschema>=3.2.0',
    ],
    project_urls={
        'Documentation': 'https://github.com/sgh370/ml-django-brain',
        'Bug Reports': 'https://github.com/sgh370/ml-django-brain/issues',
        'Source': 'https://github.com/sgh370/ml-django-brain',
    },
)
