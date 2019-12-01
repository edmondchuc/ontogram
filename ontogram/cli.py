#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from ontogram import Ontogram


@click.command()
@click.option('--format',
              default='turtle',
              metavar="['turtle', 'xml', 'nt', 'n3']",
              help='RDF serialization of input file. Default is turtle.')
@click.argument('ontology_filepath', type=click.Path(exists=True))
def main(ontology_filepath, format):
    """Ontogram CLI is a tool to generate a diagram from an OWL ontology file."""
    ontogram = Ontogram(ontology_filepath, format=format)

    ontogram.plantuml_file(ontology_filepath)
    ontogram.png_file(ontology_filepath + '.txt')
    ontogram.svg_file(ontology_filepath + '.txt')


if __name__ == '__main__':
    main()