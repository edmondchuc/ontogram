# Ontogram

[![PyPI version](https://badge.fury.io/py/ontogram.svg)](https://badge.fury.io/py/ontogram)

An OWL ontology diagram generator.

Currently it supports `owl:class`, `rdfs:subClassOf`, `owl:equivalentClass`, datatype properties and domain and range relationships. I am planning to add support for `owl:subClassOf` restrictions soon. 


## Example output

The output of [examples/tern-org.ttl](examples/tern-org.ttl).

![generated ontology diagram](examples/tern-org.ttl.txt.png)


## Installation

Install via PyPI for Python 3.

```
pip3 install ontogram
```


## Usage

### Command line application

```
$ ontogram --help

Usage: ontogram [OPTIONS] ONTOLOGY_FILEPATH

  Ontogram CLI is a tool to generate a diagram from an OWL ontology file.

Options:
  --format ['turtle', 'xml', 'nt', 'n3']
                                  RDF serialization of input file. Default is
                                  turtle.
  --help                          Show this message and exit.
```

Use Ontogram's CLI to generate diagrams of an OWL ontology.
```
ontogram ontology.ttl
```

Output will be 3 files, `ontology.ttl.txt`, `ontology.ttl.png`, `ontology.ttl.svg`.

Use the --format option to specify the RDF serialization of the ontology if it is not Turtle.


### Python library

Ontogram is a Python library and can be easily integrated with any existing Python application.

```python
from ontogram import Ontogram

# First parameter accepts a file path to the OWL ontology. 
# Second parameter tells Ontogram what RDF format the OWL ontology is in.
ontogram = Ontogram('ontology.ttl', format='turtle')

# Generate a PNG diagram from the OWl ontology and write to disk as 'ontology.ttl.txt'.
ontogram.png_file('ontology.ttl.txt')

# Same as above, but as an SVG diagram. 
ontogram.svg_file('ontology.ttl.svg')
```

See the [examples](examples) directory for example outputs.
