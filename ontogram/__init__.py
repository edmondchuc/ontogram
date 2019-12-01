from rdflib import Graph, URIRef, BNode
from rdflib.namespace import RDF, OWL, RDFS, DCTERMS
from plantuml import PlantUML

from ontogram.curies import CURIES


class Ontogram:
    """
    Ontogram class accepts an OWL ontology file and provides methods
    to produce a PlantUML-based diagram.
    """
    def __init__(self, filepath : str, format='turtle'):
        """

        :param filepath: File path of the OWL ontology file.
        :param format: RDF serialization of the OWl ontology file. Options: ['turtle', 'xml', 'nt', 'n3'].
        """
        self.g = Graph().parse(filepath, format=format)
        self._plantuml = '@startuml\n'
        self._plantuml += _get_ontology_title(self.g)
        self._plantuml += _get_subclass_relationship(self.g)
        self._plantuml += _get_class_definition(self.g)
        self._plantuml += _get_outgoing_relationship(self.g)
        self._plantuml += _get_equivalent_classes(self.g)
        self._plantuml += _get_creator(self.g)
        self._plantuml += _add_reference()
        self._plantuml += '@enduml'

    @property
    def plantuml(self):
        """Get the PlantUML text of the ontology diagram."""
        return self._plantuml

    @property
    def url(self):
        """Get the URL of the ontology from www.plantuml.com."""
        p = PlantUML(url='http://www.plantuml.com/plantuml/img/')
        return p.get_url(self.plantuml)

    def plantuml_file(self, filename):
        """Write the PlantUML text of the ontology diagram to file."""
        with open(filename + '.txt', 'w') as f:
            f.write(self.plantuml)

    @staticmethod
    def png_file(filename):
        """Write the ontology diagram to file as PNG."""
        p = PlantUML(url='http://www.plantuml.com/plantuml/img/')
        p.processes_file(filename, outfile=filename + '.png')

    @staticmethod
    def svg_file(filename):
        """Write the ontology diagram to file as SVG."""
        p = PlantUML(url='http://www.plantuml.com/plantuml/svg/')
        p.processes_file(filename, outfile=filename + '.svg')


def _get_ontology_title(g):
    for ontology in g.subjects(RDF.type, OWL.Ontology):
        for t in g.objects(ontology, RDFS.label):
            return f'title {t}\n'
    return 'title Untitled\n'


def _get_last_segment_of_uri(uri : str):
    return str(uri).split('#')[-1].split('/')[-1]


def _get_uri_namespace(uri : str):
    # Get the URI namespace by dropping the '#'.
    URI = str(uri).split('#')[0]

    if URI == str(uri):
        # If URI unchanged, it means the separator is a '/'. Go ahead and drop the word after the slash.
        suffix = URI.split('/')[-1]
        URI = URI.replace(suffix, '')
    else:
        # Append the '#' back on so it ends in a hash or slash.
        URI += '#'

    return URI


def _get_uri_prefix(uri : str, g):
    # Get the prefix of the URI.
    prefix = ''
    for k, v in CURIES.items():
        if v == uri:
            prefix = k
            return prefix

    # Didn't find a matching prefix in CURIES.
    # TODO: Do something here e.g. a lookup to prefix.cc or something else.
    for ontology, _, _ in g.triples((None, RDF.type, OWL.Ontology)):
        for preferred_prefix in g.objects(ontology, URIRef('http://purl.org/vocab/vann/preferredNamespacePrefix')):
            return preferred_prefix

    # Nothing was found, just return an empty string.
    return prefix


def _get_class_definition(g):
    classes = _get_classes(g)
    plant_uml = ''
    for owl_class, _, _ in g.triples((None, RDF.type, OWL.Class)):
        class_name = _get_last_segment_of_uri(owl_class)

        uri = _get_uri_namespace(str(owl_class))
        prefix = _get_uri_prefix(uri, g)

        assert prefix is not None, f'No prefix found for URI {uri}'

        plant_uml += f'Class "{prefix}:{class_name}" [[{str(owl_class)}]] {{\n'

        for rdf_property, _, _ in g.triples((None, RDFS.domain, owl_class)):
            for _, _, rdfs_range_value in g.triples((rdf_property, RDFS.range, None)):
                if not rdfs_range_value in classes:
                    rdf_property_namespace = _get_uri_namespace(rdf_property)
                    rdf_property_prefix = _get_uri_prefix(rdf_property_namespace, g)
                    rdf_property_name = _get_last_segment_of_uri(rdf_property)

                    rdfs_range_namespace = _get_uri_namespace(rdfs_range_value)
                    rdfs_range_property_prefix = _get_uri_prefix(rdfs_range_namespace, g)
                    rdfs_range_property_name = _get_last_segment_of_uri(rdfs_range_value)

                    plant_uml += f'[[{rdf_property} {rdf_property_prefix}:{rdf_property_name}]] : [[{rdfs_range_value} {rdfs_range_property_prefix}:{rdfs_range_property_name}]]\n'

        plant_uml += '}\n'

    return plant_uml


def _is_class_type_owl_restriction(super_class, g):
    for _, _, class_type in g.triples((super_class, RDF.type, OWL.Restriction)):
        return True
    return False


def _get_subclass_relationship(g):
    plant_uml = ''

    for owl_class, _, _ in g.triples((None, RDF.type, OWL.Class)):
        for _, _, super_class in g.triples((owl_class, RDFS.subClassOf, None)):

            # Don't show subClass relationships if it's a subClass to an OWL restriction.
            owl_restriction_bool = _is_class_type_owl_restriction(super_class, g)
            if not owl_restriction_bool:
                super_class_namespace = _get_uri_namespace(super_class)
                super_class_prefix = _get_uri_prefix(super_class_namespace, g)
                super_class_name = _get_last_segment_of_uri(super_class)

                owl_class_namespace = _get_uri_namespace(owl_class)
                owl_class_prefix = _get_uri_prefix(owl_class_namespace, g)
                owl_class_name = _get_last_segment_of_uri(owl_class)

                plant_uml += f'"{super_class_prefix}:{super_class_name}" <|-- "{owl_class_prefix}:{owl_class_name}"\n'

    return plant_uml


def _get_classes(g):
    classes = []
    for owl_class, _, _ in g.triples((None, RDF.type, OWL.Class)):
        classes.append(owl_class)
        for _, _, equivalent_class in g.triples((owl_class, OWL.equivalentClass, None)):
            classes.append(equivalent_class)
    return classes


def _get_outgoing_relationship(g):
    plant_uml = ''

    classes = _get_classes(g)

    for rdf_property, _, _ in g.triples((None, RDF.type, RDF.Property)):
        for _, _, rdfs_domain in g.triples((rdf_property, RDFS.domain, None)):
            for _, _, rdfs_range in g.triples((rdf_property, RDFS.range, None)):
                if rdfs_range in classes:
                    domain_namespace = _get_uri_namespace(rdfs_domain)
                    domain_prefix = _get_uri_prefix(domain_namespace, g)
                    domain_name = _get_last_segment_of_uri(rdfs_domain)

                    relationship_namespace = _get_uri_namespace(rdf_property)
                    relationship_prefix = _get_uri_prefix(relationship_namespace, g)
                    relationship_name = _get_last_segment_of_uri(rdf_property)

                    range_namespace = _get_uri_namespace(rdfs_range)
                    range_prefix = _get_uri_prefix(range_namespace, g)
                    range_name = _get_last_segment_of_uri(rdfs_range)

                    plant_uml += f'"{domain_prefix}:{domain_name}" --> "{range_prefix}:{range_name}" : "[[{str(rdf_property)} {relationship_prefix}:{relationship_name}]]"\n'
                break
            break

    return plant_uml


def _get_equivalent_classes(g):
    plant_uml = ''
    for owl_class, _, _ in g.triples((None, RDF.type, OWL.Class)):
        for _, _, equivalent_class in g.triples((owl_class, OWL.equivalentClass, None)):
            equivalent_class_namespace = _get_uri_namespace(equivalent_class)
            equivalent_class_prefix = _get_uri_prefix(equivalent_class_namespace, g)
            equivalent_class_name = _get_last_segment_of_uri(equivalent_class)

            owl_class_namespace = _get_uri_namespace(owl_class)
            owl_class_prefix = _get_uri_prefix(owl_class_namespace, g)
            owl_class_name = _get_last_segment_of_uri(owl_class)

            plant_uml += f'"{equivalent_class_prefix}:{equivalent_class_name}" .. "{owl_class_prefix}:{owl_class_name}"\n'
    return plant_uml


def _get_creator(g):
    plant_uml = ''

    name = None
    email = None

    for ontology, _, _ in g.triples((None, RDF.type, OWL.Ontology)):
        for creator in g.objects(ontology, DCTERMS.creator):
            if type(creator) == BNode:
                for n in g.objects(creator, URIRef('http://schema.org/name')):
                    name = n

                for e in g.objects(creator, URIRef('http://schema.org/email')):
                    email = e
            else:
                name = creator

    if name or email:
        plant_uml += 'header\n'
        if name:
            plant_uml += f'Creator: {name} '
        if email:
            plant_uml += f'({email}) \n'
        plant_uml += 'endheader\n'
    return plant_uml


def _add_reference():
    return 'center footer Generated by [[https://github.com/edmondchuc/ontogram https://github.com/edmondchuc/ontogram]]\n'
