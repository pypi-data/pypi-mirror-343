from setuptools import setup, find_packages

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name='api-client-lnx-edge',
    version='0.3.11',
    description='Client for the LNX Edge API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Lnmix/edge_api_client',
    author='Nick Tulli',
    author_email='ntulli@leadnomics.com',
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    install_requires=[
        'pytz>=2021.1',
        'requests>=2.25.1',
        'marshmallow==3.18.0'
    ],
    packages=find_packages(where='src'),
    python_requires='>=3.7'
)
