from setuptools import setup, find_packages

setup(
    name="robotframework-domretrylibrary",
    version="0.1.6",
    packages=find_packages(),
    install_requires=[
        "robotframework",
        "python-dotenv",
        "requests",
    ],
    include_package_data=True,
    description="AI-powered smart locator with retry functionality for Robot Framework using OpenAI",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Kristijan Plaushku',
    author_email='info@plaushkusolutions.com',
    url='https://github.com/plaushku/robotframework-domretrylibrary',
    classifiers=[
        'Framework :: Robot Framework',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'robotframework_listener': [
            'AIRetrySmartLocator = domretrylibrary.core:AIRetrySmartLocator'
        ]
    },
) 