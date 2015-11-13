from setuptools import setup, find_packages


setup(
    name='scrapy-bigml',
    version='0.0.1a',
    url='https://github.com/scrapy-plugins/scrapy-bigml',
    description='Scrapy pipeline for writing items to BigML datasets',
    long_description=open('README.rst').read(),
    author='Scrapy developers',
    license='BSD',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Framework :: Scrapy',
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
    requires=['scrapy (>=1.0)', 'bigml'],
)
