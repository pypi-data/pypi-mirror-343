from setuptools import setup, find_packages

setup(
    name='pymagic_HM',
    version='0.1',
    packages=find_packages(),
    install_requires=['pygame'],
    description="A library for creating magic effects in games.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown', 
    author='Houda Izem',
    author_email='houdaizem166@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
