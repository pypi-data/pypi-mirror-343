from setuptools import setup, find_packages
import os

# Read the contents of the README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="robotframework_domretrylibrary",
    version="2.5.1",
    packages=find_packages(),
    py_modules=["DomRetryLibrary"],
    install_requires=[
        "robotframework>=4.0.0",
        "python-dotenv>=0.19.0",
        "requests>=2.25.0",
    ],
    include_package_data=True,
    description="AI-powered smart locator with retry functionality for Robot Framework using OpenAI",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Kristijan Plaushku',
    author_email='info@plaushkusolutions.com',
    url='https://github.com/plaushku/robotframework-domretrylibrary',
    python_requires='>=3.7',
    classifiers=[
        'Framework :: Robot Framework',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Testing :: Acceptance',
    ],
    keywords='robotframework testing selenium webdriver ai openai',
    entry_points={
        'robotframework.libraries': [
            'DomRetryLibrary = domretrylibrary:DomRetryLibrary',
        ]
    },
) 