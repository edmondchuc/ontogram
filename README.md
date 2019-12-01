# Ontogram

Ontogram is an OWL ontology diagram generator.

This tool generates a PlantUML text file from an ontology file. Feeding the text file into PlantUML will generate a diagram of the ontology with UML syntax.

Currently it supports `owl:class`, `rdfs:subClassOf`, `owl:equivalentClass`, datatype properties and domain and range relationships. I am planning to add support for `owl:subClassOf` restrictions soon. 


## todo

- Clean the git history from the plantuml.jar
- Create pip installable of ontogram
- Create online web form
- Create rest api


## Example output

The output of [tern-org.ttl](tern-org.ttl).

![generated ontology diagram](tern-org.ttl.png)


## Run

Set up virtualenv

```
python3 -m venv venv
``` 

Activate venv

```
source venv/bin/activate
```

Install dependencies

```
pip3 install -r requirements.txt
```

Generate the PlantUML text file

```
python3 app.py ontology.ttl ontology.ttl
```

Output file will be ontology.ttl.txt


Use PlantUML to generate the diagram (Java and Graphviz required, refer to PlantUML docs for installation)

```
java -jar plantuml.jar ontology.ttl.txt
```

Output will be `tern.org.ttl.png`


To generate an SVG

```
java -jar plantuml.jar -tsvg ontology.ttl.txt
```


## Docker image for diagram generation within pyLODE

A Docker image has been created to automatically embed the generated diagram into a pyLODE document. See https://github.com/edmondchuc/docker-pylode

See the pyLODE output with the generated ontology diagram: https://ternaustralia.github.io/ontology_tern-org/