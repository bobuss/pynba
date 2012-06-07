from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()

version = '0.1'

install_requires = [
    'protobuf',
    'werkzeug',
    'setuptools-ci',
]

if sys.version_info < (2, 7):
    install_requires += ['unittest2']

setup(name='iscool_e.pynba',
    version=version,
    description="wsgi middleware for pinba",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='pinba wsgi',
    author='Xavier Barbosa',
    author_email='xavier.barbosa@iscool-e.com',
    url='git@git.iscoolapp.com:pynba.git',
    license='',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages = ['iscool_e'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=['nose-exclude'],
)
