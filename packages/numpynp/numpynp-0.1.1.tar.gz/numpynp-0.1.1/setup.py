from setuptools import setup, find_packages

setup(
    name='numpynp',  # Your package name
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,  # Important for non-.py files
    author='OMK',
    author_email='gangurdenishant07@gmail.com',
    description='A library that provides assignments as text variables',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # optional, if you host on GitHub
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
