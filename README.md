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
  --header LIST                   Comma-separated list of configuration
                                  statements, which will be split on comma and
                                  included as a set of lines in the PlantUML's
                                  header section.

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
# Third parameter allows to pass whatever list of PlantUML predicates
# you may pass to configure the diagram.
ontogram = Ontogram('ontology.ttl', format='turtle', headers=['left to right direction'])

# Generate a PNG diagram from the OWl ontology and write to disk as 'ontology.ttl.txt.png'.
ontogram.png_file('ontology.ttl.txt')

# Same as above, but as an SVG diagram 'ontology.ttl.txt.svg'.
ontogram.svg_file('ontology.ttl.txt')
```

See the [examples](examples) directory for example outputs.


### Headers parameter

With the `headers` parameter, you can configure the diagram shape.
Ontogram uses the [PlantUML](https://plantuml.com) library under the hood
to draw the output as a "class diagram".

PlantUML takes a human-readable script describing the schema as an input.
This is the `.txt` file that Ontogram produces, you can take a look at it with
any text editor.
PlantUML allows to add several lines in the beginning of the script,
after the `@startuml` tag.

The `headers` parameter of Ontogram allows you to pass configuration statements
to the PlantUML script.
For instance, to change diagram orientation, you can pass, eiher:
- `--headers='left to right direction'`, or
- `--headers='top to bottom direction'`.

You may pass several statements, separated by a comma.
They will be inserted as separated lines in the header section,
for example:
`--headers='left to right direction,scale 750 width'`

See the [PlantUML](https://plantuml.com/en/guide) documentation for more
information and configuration ideas.

