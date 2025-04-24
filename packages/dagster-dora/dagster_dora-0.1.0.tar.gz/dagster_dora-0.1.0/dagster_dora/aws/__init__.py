"""Dora Dagster Assets Module for aws."""
from os import environ

# Catalog environment variable.
CATALOG = environ.get("CATALOG", "GlueCatalog")
