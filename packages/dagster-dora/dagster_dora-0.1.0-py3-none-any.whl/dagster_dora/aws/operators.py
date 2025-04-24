"""Dagster Dora operators.

This module contains functions and utilities for interacting with AWS resources
and managing asset metadata within the Dagster framework.
"""
from hashlib import sha1
from time import sleep
from typing import Tuple, Iterator
from boto3 import client
from pyiceberg.catalog import load_catalog
from pyiceberg.table import Table as IcebergTable
from pyiceberg.table.snapshots import Snapshot

from dagster import (
    AssetExecutionContext,
    MetadataValue,
    MaterializeResult,
    TableColumn,
    TableSchema
)
from dagster_aws.pipes import PipesLambdaClient

from . import CATALOG
from .resources import AwsResources

athena = client('athena')

def get_asset_resources(asset: str, stack: AwsResources) -> Iterator[Tuple[str, str]]:
    """Retrieve resources associated with a given asset.

    Args:
        asset (str): The name of the asset.
        stack (AwsResources): The AWS resources stack.

    Yields:
        Iterator[Tuple[str, str]]: An iterator of resource type and resource value pairs.
    """
    for _, values in stack.resources:
        for _asset, value in values['resources'].items():
            if _asset == asset:
                yield ('sql',values['sql'])
                for rs_key, rs_value in value.items():
                    if rs_key == 'lambda':
                        yield ('lambda', rs_value.split(":", maxsplit=-1)[-1])
                    if rs_key == 'dagster/table_name':
                        yield ('table', rs_value)

def iceberg_schema(table: IcebergTable) -> Iterator[TableColumn]:
    """Generate schema metadata for the asset.

    Args:
        table (IcebergTable): The Iceberg table object.

    Returns:
        Iterator[TableColumn]: An iterator of table columns.
    """
    for _field in table.schema().fields:
        yield TableColumn(
            name=str(_field.name),
            type=str(_field.field_type),
            description=str(_field.doc),
        )

def iceberg_metadata(identifier: str, snapshot: bool) -> Iterator[Tuple[str, str]]:
    """Generate metadata for the asset materialization.

    Args:
        identifier (str): The identifier of the Iceberg table.
        snapshot (bool): Flag indicating whether to include snapshot metadata.

    Yields:
        Iterator[Tuple[str, str]]: An iterator of metadata key-value pairs.
    """
    catalog = load_catalog(CATALOG, **{"type": "glue"})
    _tbl = catalog.load_table(identifier)
    yield ("dagster/column_schema", TableSchema(columns=list(iceberg_schema(table=_tbl))))
    if snapshot:
        _snapshot = _tbl.current_snapshot()
        if isinstance(_snapshot, Snapshot):
            yield ("snapshot", MetadataValue.json(
                data=_snapshot.model_dump_json()))
            yield ("dagster/row_count", MetadataValue.int(
                value=int(_snapshot.summary.get("total-records"))))
            yield ("dagster/partition_row_count", MetadataValue.int(
                value=int(_snapshot.summary.get("added-records"))))
        else:
            yield ("dagster/row_count", MetadataValue.int(0))
            yield ("dagster/partition_row_count", MetadataValue.int(0))

def update_results(result: MaterializeResult, identifier: str) -> MaterializeResult:
    """Update materialization results with additional metadata.

    Args:
        result (MaterializeResult): The initial materialization result.
        identifier (str): The identifier of the Iceberg table.

    Returns:
        MaterializeResult: The updated materialization result.
    """
    # Add metadata from Athena
    if result.metadata.get('QueryExecutionId') is not None:
        _state = 'QUEUED'
        while(_state == 'QUEUED' or _state == 'RUNNING'):
            _response = athena.get_query_execution(
                QueryExecutionId=result.metadata.get('QueryExecutionId').text
            )['QueryExecution']
            _state = _response['Status']['State']
            sleep(1) # wait for 1 second to avoid throttling
        result.metadata['Query']=MetadataValue.md(_response['Query'])
        result.metadata['Status']=MetadataValue.text(_state)
        result.metadata['Total Execution Time In Millis']=MetadataValue.int(
            int(_response['Statistics']['TotalExecutionTimeInMillis']))
        result.metadata['Data Scanned In Bytes']=MetadataValue.int(
            int(_response['Statistics']['DataScannedInBytes']))
        if _state == 'FAILED' or _state == 'CANCELLED':
            raise ValueError(f"Query failed: {_response['Status']['AthenaError']}")
    # Add metadata from iceberg
    for _key, _value in iceberg_metadata(identifier, result.metadata.get('snapshot') is None):
        result.metadata[_key]=_value
    return result

def asset_file_op(
        context: AssetExecutionContext,
        lambda_pipes: PipesLambdaClient,
        stack: AwsResources) -> MaterializeResult:
    """Dora asset operator for processing files.

    Args:
        context (AssetExecutionContext): The execution context for the asset.
        lambda_pipes (PipesLambdaClient): The Lambda client for invoking AWS Lambda functions.
        stack (AwsResources): The AWS resources stack.

    Returns:
        MaterializeResult: The result of the asset materialization process.
    """
    _asset_name = context.asset_key.parts[0]
    context.log.debug("Table: %s", _asset_name)
    _rs = dict(get_asset_resources(_asset_name, stack))
    context.log.info("resources: %s", _rs)
    _time, _file = str(context.partition_key).split('|')
    context.log.info("%s|%s", _time, _file)
    _dag = sha1(_file.encode()).hexdigest()
    context.log.info("%s", _dag)
    return update_results(lambda_pipes.run(
        context=context,
        function_name=_rs['lambda'],
        event={
            'dag':_dag,
            'table':_asset_name,
            'file':_file,
            'time':_time,
            'sql':_rs['sql'],
            },
    ).get_materialize_result(), _rs['table'])
