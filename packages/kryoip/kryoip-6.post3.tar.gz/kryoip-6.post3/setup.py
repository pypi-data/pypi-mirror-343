from setuptools import setup, find_packages

setup(
    name='kryoip',
    version='6-3',
    packages=find_packages(),
    install_requires=[],
    author='PDX',
    author_email='valkdevices@gmail.com',
    description='A library for simplifying IP handling in code',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://www.valkdevices.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
