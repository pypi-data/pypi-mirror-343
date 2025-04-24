# NUVA Utilities
NUVA is the unified nomenclature of vaccines.

It is a common good promoted and published by the _International Vaccine Codification Initiative_ at https://ivci.org/nuva.

This package proposes a set of tools for handling NUVA as a RDF graph. It relies upon RDFLib.

The current version exposes 7 methods:
  - **nuva_version** returns the version number of the last published release of NUVA
  - **nuva_core_graph** returns a RDF graph representing the core concepts of NUVA: vaccines and valences.
  - **nuva_get_vaccines** returns the list of all NUVA codes in the graph, possibly limited to abstract concepts only (excluding branded products)
  - **nuva_add_codes_to_graph** complements a NUVA graph with alignments between NUVA concepts and codes from another code system, typically extracted from a CSV mapping file.
  - **nuva_add_lang** complements a NUVA graph with additional triples providing the translation of NUVA concepts to another language than English.
  - **nuva_translate** returns correspondence tables between two languages already included in the graph.
  - **nuva_optimize** determines the optimal representation of all NUVA concepts in a given code system. It returns optimal mappings from NUVA to the code system, from the code system to NUVA, and metrics on the completeness, precision and redundancy of the code system.
  