# -*- coding: utf-8 -*-
"""Dora Pipeline CDK constructs."""
import base64
from typing import Iterator
from json import dumps
from os import path, environ

from constructs import Construct
from aws_cdk import (
    Aws,
    Duration,
    CfnOutput,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_events as events,
    aws_glue as glue,
    aws_ecr as ecr,
    aws_kms as kms,
    aws_lakeformation as lfm,
    aws_events_targets as targets,
)

from dora_core.utils import logger
from dora_core.asset import Job, Table
from dora_core.conf import Profile

from dora_aws.utils import s3_bucket_key
from dora_aws.plugins.volumes.s3 import Profile as S3Vol

from .engines import Lambda

log = logger(__name__)

class Sensors(Construct):
    """Dora sensors construct class.

    This class creates an SQS queue and an EventBridge rule for a given table.
    The rule triggers the queue when an object is created in the specified S3 bucket.
    """
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **{})
        _table:Table = kwargs["table"]
        self.queue = self.create_queue(_table)
        self.rule = self.create_rule(_table)
        self.rule.add_target(target=targets.SqsQueue(queue=self.queue))

    def create_queue(self, table:Table) -> sqs.Queue:
        """Create the SQS queue.

        Args:
            table (Table): The table for which the queue is being created.

        Returns:
            sqs.Queue: The created SQS queue.
        """
        return sqs.Queue(
            scope=self,
            id=f"{table.name}-sqs",
            queue_name=table.name,
            visibility_timeout=Duration.seconds(300),
        )

    def create_rule(self, table:Table) -> events.Rule:
        """Create the EventBridge rule.

        Args:
            table (Table): The table for which the rule is being created.

        Returns:
            events.Rule: The created EventBridge rule.
        """
        return events.Rule(
            scope=self,
            id=f"{table.name}-ebr",
            event_pattern=events.EventPattern(**self._event_rule(table))
            )

    def _event_rule(self, table: Table) -> dict:
        """Create source pattern for event rule.

        Args:
            table (Table): The table for which the event rule pattern is being created.

        Returns:
            dict: The event rule pattern.
        """
        _src = table.source.split("/")
        if not _src[0].startswith("s3"):
            raise NotImplementedError("Only s3 source is supported")
        # File key path
        _key = "/".join(_src[3:])
        if "*" in _key:  # Idicates the use of wildcard
            _filter = {"wildcard": _key}
        else:  # Otherwise, use prefix (starts with)
            _filter = {"prefix": _key}
        return {
            "source": ["aws.s3"],
            "detail_type": ["Object Created"],
            "detail": {
                "bucket": {"name": [_src[2]]},
                "object": {"key": [_filter]},
            },
        }

class Workflow(Construct):
    """Dora workflow construct class.

    This class handles the creation of various AWS resources needed for a data processing job,
    including Glue tables, SQS queues, EventBridge rules, and Lambda functions.
    """
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **{})
        self.file:str = kwargs["file"]
        self.job:Job = kwargs["job"]
        self.cmk:kms.Key = kwargs["cmk"]
        self.repository:ecr.Repository = kwargs["repository"]
        self.resources()

    @staticmethod
    def check_duplicate_asset_names(assets:dict) -> bool:
        """Check for duplicate asset names.

        Args:
            assets (dict): The assets to check for duplicates.

        Returns:
            bool: True if no duplicates are found, otherwise raises a ValueError.
        """
        _asset_list = set()
        _volum_list = set()
        for rs in assets['resources']:
            _asset_list.add(rs)
            _volum_list.add(assets['resources'][rs]['volumes'].get('location'))
            _volum_list.add(assets['resources'][rs]['volumes'].get('source'))
        _volumes = [_v for _v in _volum_list if _v in _asset_list]
        if len(_volumes) > 0:
            log.error("The following volumes have the same names of others table assets: %s", _volumes)
            log.warning("Please rename the volumes to avoid conflicts.")
            log.info("Remamber the dots are replaced by underscores to create the final name of the data assets")
            raise ValueError(f"Duplicate asset names: {','.join(_volumes)}")
        return True

    def resources(self) -> CfnOutput:
        """Generate resources and define dependencies.

        Returns:
            CfnOutput: The CloudFormation output containing the stack resources.
        """
        _profile = Profile.load()
        _outputs = dict(
            file=path.join(environ.get("DORA_BUILD_TARGET_DIR","target"), self.file),
            sql=base64.b64encode(self.job.sql.encode('utf-8')).decode('utf-8'),
            job=self.job.name,
            resources=dict())
        for _table in self.job.tables:
            _outputs["resources"].update({_table.name:dict()})
            for _resource in self.create_tables(_table):
                _outputs["resources"][_table.name]['volumes'] = dict()
                for _profile_output in _profile.ouputs[_profile.target]:
                    if isinstance(_profile_output, S3Vol):
                        _uri = _profile_output.render()
                        if _uri == _table.source:
                            _outputs["resources"][_table.name]['volumes'].update(
                                {"source": _profile_output.name})
                        if _uri == _table.location:
                            _outputs["resources"][_table.name]['volumes'].update(
                                {"location": _profile_output.name})
                if isinstance(_resource, glue.CfnTable):
                    _outputs["resources"][_table.name].update(
                        {"dagster/table_name": f"{_resource.database_name}.{_resource.ref}"})
                elif isinstance(_resource, Sensors):
                    _outputs["resources"][_table.name].update(
                        {"queue": _resource.queue.queue_arn})
                    _outputs["resources"][_table.name].update(
                        {"rule": _resource.rule.rule_arn})
                elif isinstance(_resource, Lambda):
                    _outputs["resources"][_table.name].update(
                        {"lambda": _resource.function.function_arn})
                else:
                    _outputs["resources"][_table.name].update(
                        {_resource.node.id: _resource.ref})
        if self.check_duplicate_asset_names(_outputs):
            return CfnOutput(
                scope=self,
                id=f"{self.job.name}-out",
                key=self.job.name,
                value=dumps(_outputs),
                description=f"Stack resources for {self.job.name}",
            )

    def create_tables(self, table:Table) -> Iterator[glue.CfnTable]:
        """Create Glue tables and associated resources.

        Args:
            table (Table): The table for which resources are being created.

        Yields:
            Iterator[glue.CfnTable]: The created Glue table and associated resources.
        """
        log.debug("TABLE[%s]", table.identifier)
        _tbl = glue.CfnTable(
            scope=self,
            id=f"glue:table:{table.name}",
            catalog_id=Aws.ACCOUNT_ID,
            database_name=table.database,
            open_table_format_input=self._open_table_format_input_property(),
            table_input=glue.CfnTable.TableInputProperty(
                name=table.table,
                table_type="EXTERNAL_TABLE",
                parameters={"classification": "iceberg"},
                # Not supported by CDK (couses HIVE_UNSUPPORTED_FORMAT when updated)
                # description=table.schema_comment,
                storage_descriptor=glue.CfnTable.StorageDescriptorProperty(
                    location=table.location,
                    columns=list(self._column_property(table)))))
        yield _tbl
        # Only create sensors for tables with source
        if table.source is not None:
            log.debug("SENSORS[%s]", table.identifier)
            _sns = Sensors(self, f"{table.name}-sns", table=table)
            _sns.node.add_dependency(_tbl)
            yield _sns
        if table.deployment_type == 'serverless':
            log.debug("ENGINE-%s[%s]", table.deployment_type, table.identifier)
            _func = Lambda(self, f"{table.name}-func",
                            repository=self.repository,
                            cmk=self.cmk,
                            table=table)
            _func.node.add_dependency(_tbl)
            yield _func
        else:
            raise NotImplementedError(f"Deployment type {table.deployment_type} not implemented")


    def _column_property(self, table:Table) -> Iterator[glue.CfnTable.ColumnProperty]:
        """Generate column properties for table columns.

        Args:
            table (Table): The table for which column properties are being generated.

        Yields:
            Iterator[glue.CfnTable.ColumnProperty]: The column properties.
        """
        for col in table.meta_fields():
            yield glue.CfnTable.ColumnProperty(
                name=str(col.name).lower(),
                type=str(col.field_type).replace(' ',''),
                comment=str(col.doc).strip()
            )

    @staticmethod
    def _open_table_format_input_property() -> glue.CfnTable.OpenTableFormatInputProperty:
        """Generate the open table format input property.

        Returns:
            glue.CfnTable.OpenTableFormatInputProperty: The open table format input property.
        """
        return glue.CfnTable.OpenTableFormatInputProperty(
            iceberg_input=glue.CfnTable.IcebergInputProperty(
                metadata_operation="CREATE",
                version="2"
            )
        )

    def create_optimizer_role(self, table:Table) -> iam.Role:
        """Create the optimizer role.

        Args:
            table (Table): The table for which the optimizer role is being created.

        Returns:
            iam.Role: The created IAM role.
        """
        _bkt, _ = s3_bucket_key(table.location)
        _role = iam.Role(
            scope=self,
            id=f"{table.name}-Optimizer-Role",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"))
        _role.add_to_policy(iam.PolicyStatement(
            resources=[f"arn:aws:s3:::{_bkt}/*"],
            actions=["s3:PutObject", "s3:GetObject", "s3:DeleteObject"]
        ))
        _role.add_to_policy(iam.PolicyStatement(
            resources=[f"arn:aws:s3:::{_bkt}"],
            actions=["lakeformation:GetDataAccess"]
        ))
        _role.add_to_policy(iam.PolicyStatement(
            resources=["*"],
            actions=["s3:ListBucket"]
        ))
        _role.add_to_policy(iam.PolicyStatement(
            resources=[
                f"arn:aws:glue:{Aws.REGION}:{Aws.ACCOUNT_ID}:catalog",
                f"arn:aws:glue:{Aws.REGION}:{Aws.ACCOUNT_ID}:database/{table.database}",
                f"arn:aws:glue:{Aws.REGION}:{Aws.ACCOUNT_ID}:table/{table.database}/{table.table}",
                ],
            actions=["glue:UpdateTable", "glue:GetTable"]
        ))
        _role.add_to_policy(iam.PolicyStatement(
            resources=[
                f"arn:aws:logs:{Aws.REGION}:{Aws.ACCOUNT_ID}:log-group:/aws-glue/iceberg-compaction/logs:*",
                f"arn:aws:logs:{Aws.REGION}:{Aws.ACCOUNT_ID}:log-group:/aws-glue/iceberg-retention/logs:*",
                f"arn:aws:logs:{Aws.REGION}:{Aws.ACCOUNT_ID}:log-group:/aws-glue/iceberg-orphan-file-deletion/logs:*",
                ],
            actions=["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        ))
        lfm.CfnPermissions(
            scope=self,
            id=f"{table.name}-optimizer-lf",
            data_lake_principal=lfm.CfnPermissions.DataLakePrincipalProperty(
                data_lake_principal_identifier=_role.role_arn
            ),
            resource=lfm.CfnPermissions.ResourceProperty(
                database_resource=lfm.CfnPermissions.DatabaseResourceProperty(
                    catalog_id=Aws.ACCOUNT_ID,
                    name=table.database
                ),
                table_resource=lfm.CfnPermissions.TableResourceProperty(
                    catalog_id=Aws.ACCOUNT_ID,
                    database_name=table.database,
                    name=table.table
                ),
            ),
            permissions=["ALL"],
            permissions_with_grant_option=["ALL"]
        )
        return _role

    def create_optimizer(self, table:Table, resource:glue.CfnTable) -> glue.CfnTableOptimizer:
        """Optimize the workflow.

        Args:
            table (Table): The table for which the optimizer is being created.
            resource (glue.CfnTable): The Glue table resource.

        Returns:
            glue.CfnTableOptimizer: The created table optimizer.
        """
        _role = self.create_optimizer_role(table)
        _optimizer = glue.CfnTableOptimizer(
            scope=self,
            id=f"{table.name}-TableOptimizer",
            catalog_id=Aws.ACCOUNT_ID,
            database_name=table.database,
            table_name=table.table,
            type="compaction",
            table_optimizer_configuration = glue.CfnTableOptimizer.TableOptimizerConfigurationProperty(
                enabled=True,
                role_arn=_role.role_arn,
            ),
        )
        _optimizer.node.add_dependency(_role)
        _optimizer.node.add_dependency(resource)
        return _optimizer
