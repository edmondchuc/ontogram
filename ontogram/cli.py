#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from ontogram import Ontogram


@click.command()
@click.option('--format',
              default='turtle',
              metavar="['turtle', 'xml', 'nt', 'n3']",
              help='RDF serialization of input file. Default is turtle.')
@click.option('--header',
              default='',
              metavar='LIST',
              help="Comma-separated list of configuration statements, which will be split on comma and included as a set of lines in the PlantUML's header section.")
@click.argument('ontology_filepath', type=click.Path(exists=True))
def main(ontology_filepath, format, header):
    """Ontogram CLI is a tool to generate a diagram from an OWL ontology file."""

    headers = header.split(',')
    print('\n'.join(headers))

    ontogram = Ontogram(ontology_filepath, format=format, headers=headers)

    ontogram.plantuml_file(ontology_filepath) # Saves with extension: .txt
    ontogram.png_file(ontology_filepath + '.txt') # Saves with extension: .png
    ontogram.svg_file(ontology_filepath + '.txt') # Saves with extension: .svg


if __name__ == '__main__':
    main()
