from setuptools import (
    find_packages,
    setup,
)


file_name = 'VERSION'
with open(file_name, 'r') as f:
    VERSION = f.read()

setup(
    name='erasure',
    version=VERSION,
    py_modules=['erasure'],
    description="""A python library to interact with the erasure protocol.""",
    long_description_markdown_filename='README.md',
    author='Ankit Chiplunkar',
    author_email='ankitchiplunkar@gmail.com',
    url='https://github.com/ankitchiplunkar/erasure.py',
    include_package_data=True,
    python_requires='>=3.6, <4',
    keywords='ethereum',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
