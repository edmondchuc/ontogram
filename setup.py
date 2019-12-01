import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ontogram",
    version="0.1.0",
    author="Edmond Chuc",
    author_email="edmond.chuc@gmail.com",
    description="Ontogram is an OWL ontology diagram generator.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edmondchuc/ontogram",
    packages=setuptools.find_packages(),
    classifiers=[
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    entry_points={'console_scripts': ['ontogram = ontogram.cli:main']},
    install_requires=['rdflib', 'click', 'plantuml'],
)