import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='threatingestor',
    version='1.0.0',
    include_package_data=True,
    install_requires=[],
    extras_require={
        ':python_version <= "2.7"': [
            'ipaddress',
        ],
        ':python_version >= "3.0"': [
            'sgmllib3k',
        ],
    },
    entry_points={
          'console_scripts': [
              'threatingestor = threatingestor:main'
          ]
    },
    license='GPL',
    description='Extract and aggregate IOCs from threat feeds.',
    long_description=README,
    url='https://github.com/InQuest/ThreatIngestor',
    author='InQuest Labs',
    author_email='labs@inquest.net',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6'
        'Programming Language :: Python :: 3.7'
        'Programming Language :: Python :: 3 :: Only'
        'Topic :: Security',
        'Topic :: Internet',
    ],
)
