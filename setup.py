import os

from setuptools import setup


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open('README.rst', 'r') as f:
    README = f.read()

with open('VERSION', 'r') as vfile:
    VERSION = vfile.read().strip()


setup(
    name='django-ssl-auth',
    version=VERSION,
    description='Django SSL Client Authentication',
    long_description=README,
    author='Kimmo Parviainen-Jalanko',
    author_email='kimvais@ssh.com',
    maintainer='Joey Wilhelm',
    maintainer_email='tarkatronic@gmail.com',
    license='MIT',
    url='https://github.com/tarkatronic/django-ssl-auth/',
    download_url='https://github.com/tarkatronic/django-ssl-auth/archive/master.tar.gz',
    packages=['django_ssl_auth'],
    include_package_data=True,
    install_requires=['Django>=1.8'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe=False,
    test_suite='runtests.runtests'
)
