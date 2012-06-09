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
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: Log Analysis",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Page Counters",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        "Topic :: Utilities"
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
