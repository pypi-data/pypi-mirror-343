"""Asset definitions for the Dora pipeline."""
from typing import Optional, List, Any, Generator, Iterator, Tuple
from os import getcwd, path
from base64 import b64decode

from sqlglot import exp
from pydantic import Field, BaseModel, ConfigDict
import dagster as dg

from dora_core.asset import Job, Table
from dora_core.engine import Engine, EngineType, CheckType
from dora_core.parser import DoraDialect
from dora_core.conf import Profile
from dora_core.utils import logger
from dora_aws.plugins.volumes.s3 import Profile as S3Vol

from .operators import asset_file_op
from .evaluators import queue_sensor_eval, get_queue_url

log = logger(__name__)

class DoraAssets(BaseModel):
    """Factory class for creating Dora assets, jobs, sensors, and volumes.

    This class is responsible for generating and managing Dora assets, jobs, sensors, and volumes
    based on the provided resources and configurations.

    Attributes:
        resources (Generator): Dora stack resources.
        deps (Optional[List[dg.AssetsDefinition]]): Asset dependencies.
        selection (Optional[List[str]]): Job selection.
        group_name (Optional[str]): Asset group name.
        profile (Profile): Dora profile.
        assets (List[Any]): List of Dora assets.
        jobs (List[Any]): List of Dora jobs.
        sensors (List[Any]): List of Dora sensors.
        volumes (List[Any]): List of Dora volumes.
    """

    resources:Generator = Field(description="Dora stack resources")
    deps:Optional[List[dg.AssetsDefinition]] = Field(description="Asset dependencies", default=None)
    selection:Optional[List[str]] = Field(description="Job selection", default=None)
    group_name:Optional[str] = Field(description="Asset group name", default=None)

    profile: Profile = Field(description="Dora profile", default=None, init=False)
    assets: List[Any] = Field(description="Dora assets", default=None, init=False)
    jobs: List[Any] = Field(description="Dora jobs", default=None, init=False)
    sensors: List[Any] = Field(description="Dora sensors", default=None, init=False)
    volumes: List[Any] = Field(description="Dora volumes", default=None, init=False)

    model_config = ConfigDict(arbitrary_types_allowed=True, extra='allow')

    def model_post_init(self, *args, **kwargs):  # pylint: disable=unused-argument
        """Post-initialization method to load profile and generate assets.

        This method is called after the model initialization to load the Dora profile and generate
        the assets, jobs, and sensors based on the provided resources.
        """
        self.profile = Profile.load()
        self.assets = list()
        self.jobs = list()
        self.sensors = list()
        if self.deps is None:
            self.deps = list()
        # Generate assets based on the resources
        self._generate_assets()

    @property
    def asset_names(self) -> Iterator[str]:
        """Iterator for asset names.

        Yields:
            Iterator[str]: An iterator of asset names.
        """
        for _asset in self.assets:
            yield _asset.key.parts[0]
        for _dep in self.deps:
            yield _dep.key.parts[0]

    def _asset_description(self, table:Table) -> str:
        """Generate a description for the asset based on the table.

        Args:
            table (Table): The table object.

        Returns:
            str: The asset description, including the SQL query.
        """
        _query = table.query(dialect=DoraDialect, pretty=True)
        return f"{table.description}\n```sql\n{_query}\n```"

    def _asset_partition(self, table:Table, resources:dict) -> dg.DynamicPartitionsDefinition:
        """Generate partition definition for the asset.

        Args:
            table (Table): The table object.
            resources (dict): The resources dictionary.

        Returns:
            dg.DynamicPartitionsDefinition: The partition definition.
        """
        _sqs = resources['resources'][table.name].get('queue')
        if _sqs is not None:
            return dg.DynamicPartitionsDefinition(name=table.name)
        for _ref in table.upstream_assets:
            return dg.DynamicPartitionsDefinition(name=_ref)

    def _asset_metadata(self, table:Table, resources:dict) -> Iterator[Tuple[str, dg.MetadataValue]]:
        """Generate metadata for the asset.

        Args:
            table (Table): The table object.
            resources (dict): The resources dictionary.

        Returns:
            Iterator[Tuple[str, dg.MetadataValue]]: Iterator of metadata key-value pairs.
        """
        for _key, _value in resources['resources'][table.name].items():
            yield (_key,dg.MetadataValue.text(str(_value)))
        yield ("dagster/code_references", dg.CodeReferencesMetadataValue(
            code_references=[
                dg.LocalFileCodeReference(
                    file_path=path.join(getcwd(),resources.get("file")),
                    label="SQL file")
                ]))
        yield ("dagster/uri", dg.MetadataValue.text(table.location))

    def _asset_checks(self, eng:Engine) -> Iterator[dg.AssetCheckSpec]:
        """Generate checks for the asset.

        Args:
            eng (Engine): The engine object.

        Returns:
            Iterator[dg.AssetCheckSpec]: Iterator of asset check specifications.
        """
        for _checks in [eng._test_checks, eng._test_nulls, eng._test_uniques]: #pylint: disable=protected-access
            for _type, _check in _checks():
                yield dg.AssetCheckSpec(
                    name=str(_check.find(exp.Identifier).this).removeprefix(_type.name+"_"),
                    blocking=_type == CheckType.FAIL,
                    description=f"```sql\n{_check.sql()}\n```",
                    asset=dg.AssetKey(eng.table.name))
        if eng.table.is_query_star:
            yield dg.AssetCheckSpec(
                name="Unmapped",
                blocking=False,
                description="Unmapped columns found in the file",
                asset=dg.AssetKey(eng.table.name))

    def _asset_dependencies(self, table:Table, volumes:dict) -> Iterator[str]:
        """Generate dependencies for the asset.

        Args:
            table (Table): The table object.
            volumes (dict): The volumes dictionary.

        Returns:
            Iterator[str]: Iterator of asset dependencies.
        """
        for _dep in table.upstream_assets:
            yield dg.AssetDep(dg.AssetKey(_dep))
        for volume, asset in volumes.items():
            if asset in [_d_.key.path[0] for _d_ in self.deps]:
                # Use the asset definition provided by the user
                yield dg.AssetDep(dg.AssetKey(asset))
            else:
                if volume == 'source':
                    for output in self.profile.ouputs[self.profile.target]:
                        if output.name == asset:
                            if isinstance(output, S3Vol):
                                self.assets.append(
                                    dg.AssetSpec(
                                        key=dg.AssetKey(output.name),
                                        description=output.render(),
                                        #Accepted values ^[A-Za-z0-9_]+$
                                        group_name=output.bucket.replace('.','_'),
                                        kinds={"s3", output.format},
                                        ))
                            else:
                                log.warning("Unsupported volume type: %s", type(output))
                                yield dg.AssetDep(dg.AssetKey(asset))
                    yield dg.AssetDep(dg.AssetKey(asset))

    def _generate_sensors(self, job:dg.JobDefinition, table:Table, resources:dict):
        """Generate sensors for the asset.

        Args:
            job (dg.JobDefinition): The job definition.
            table (Table): The table object.
            resources (dict): The resources dictionary.
        """
        _resources = resources['resources'][table.name]
        _sqs = _resources.get('queue')
        if _sqs is not None:
            _src = _resources['volumes'].get('source')
            _uri = str()
            for _out in self.profile.ouputs[self.profile.target]:
                if _out.name == _src:
                    _uri = _out.render()
            self.sensors.append(
                dg.SensorDefinition(
                    name=f"{_src}_sensor",
                    description=_resources.get('rule'),
                    job=job,
                    tags={"type": "sqs"},
                    evaluation_fn=queue_sensor_eval,
                    default_status=dg.DefaultSensorStatus.RUNNING,
                    metadata={
                        'sqs': dg.MetadataValue.text(get_queue_url(_sqs)),
                        'volume': dg.MetadataValue.text(_src),
                        'uri': dg.MetadataValue.text(_uri),
                        'target': dg.MetadataValue.text(table.name),
                        },
                    ))

    def _generate_assets(self):
        """Generate assets based on the provided resources.

        This method iterates over the provided resources and generates the corresponding assets,
        jobs, and sensors.
        """
        for _job_name, _resources in self.resources:
            print(_job_name, _resources)
            _sql = b64decode(_resources.get("sql")).decode('utf-8')
            _job = Job(name=_job_name, sql=_sql)
            # Filter jobs by the selectin provided by the user
            if self.selection is not None:
                if _job_name not in self.selection: #pylint: disable=unsupported-membership-test
                    continue
            # Create jobs definition
            self.jobs.append(
                dg.define_asset_job(
                    name=_job_name,
                    description=f"```sql\n{_sql}\n```",
                    selection=dg.AssetSelection.assets(*[t.name for t in _job.tables]),
                    metadata={"sql": dg.MetadataValue.path(_resources.get("file"))},
                    # limits concurrent assets to 1
                    config={"execution":{"config":{"multiprocess":{"max_concurrent":1}}}}
                )
            )
            # Create table assets for each table in the sql job
            for _table in _job.tables:
                self.assets.append(
                    dg.asset(
                        compute_fn=asset_file_op,
                        name=_table.name,
                        description=self._asset_description(_table),
                        kinds={"aws","iceberg","sql"},
                        owners=[_table.properties(source=False).get('owner','None')],
                        group_name=self.group_name,
                        deps=list(self._asset_dependencies(
                            table=_table,
                            volumes=_resources["resources"][_table.name].get("volumes"))),
                        metadata=dict(self._asset_metadata(_table, _resources)),
                        partitions_def=self._asset_partition(table=_table,resources=_resources),
                        check_specs=list(self._asset_checks(
                            eng=Engine(job=_job, table=_table, engine=EngineType.DUCKDB))),
                    ))
                # Add table sensors
                self._generate_sensors(job=self.jobs[-1], table=_table, resources=_resources)
