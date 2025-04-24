"""Dora CDK constructs"""
from typing import Iterator, Tuple
from os import path, environ
from pathlib import Path

from constructs import Construct
from aws_cdk import (
    Aws,
    Duration,
    RemovalPolicy,
    aws_kms as kms,
    aws_iam as iam,
)
from dora_core.asset import Job
from dora_core.conf import Profile
from dora_core.render import Sources
from dora_core.utils import logger, find_files

from .utils import rm_dir
from .catalog import Databases, Containers
from .pipeline import Workflow

log = logger(__name__)

class Dora(Construct):
    """Dora construct class."""
    def __init__(self, scope: Construct, construct_id: str, profile:str=None, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Load the profile project configuration.
        self.profile = Profile.load(profile)
        # Container repository
        self.containers = Containers(self, "containers")
        # KMS Customer managed key
        self.cmk = self.create_cmk()
        # Reads and stores SQL jobs.
        self.jobs = dict(self._read_sqls())
        # Create databases.
        self.databases = Databases(self, "databases", jobs=self.jobs)
        # Creates the workflows for each job.
        self.workflows = list(self.create_workflows())

    def create_cmk(self) -> kms.Key:
        """Create a KMS Customer Managed Key."""
        return kms.Key(
            scope=self,
            id="cmk",
            alias=f"{self.profile.name}-cmk",
            description=f"Customer Managed Key for {self.profile.name} stack",
            enable_key_rotation=True,
            removal_policy=RemovalPolicy.DESTROY,
            rotation_period=Duration.days(365),
            policy=iam.PolicyDocument(
                statements=[
                    iam.PolicyStatement(
                        sid="Enable IAM User Permissions",
                        actions=["kms:*"],
                        effect=iam.Effect.ALLOW,
                        resources=["*"],
                        principals=[iam.AccountPrincipal(account_id=Aws.ACCOUNT_ID)]
                    ),
                    iam.PolicyStatement(
                        actions=[
                            "kms:Encrypt",
                            "kms:Decrypt",
                            "kms:ReEncrypt*",
                            "kms:GenerateDataKey*",
                            "kms:CreateGrant",
                            "kms:DescribeKey",
                        ],
                        effect=iam.Effect.ALLOW,
                        sid="Allow access through AWS Lambda for all principals in the account that are authorized to use AWS Lambda",
                        resources=["*"],
                        principals=[iam.AnyPrincipal()],
                        conditions={
                            "StringEquals": {
                                "kms:CallerAccount": Aws.ACCOUNT_ID,
                                "kms:ViaService": "lambda.us-east-1.amazonaws.com"
                            }
                        }
                    ),
                ]
            )
        )

    def _read_sqls(self) -> Iterator[Tuple[str, Job]]:
        """Read SQL files.

        Reads the SQL files and renders them using the configured sources in the profile.

        Yields:
            Iterator[Tuple[str, Job]]: An iterator of tuples containing the file path and the SQL job.
        """
        target_dir = environ.get("DORA_BUILD_TARGET_DIR","target")
        rm_dir(target_dir) # remove the target directory to recreate all the files
        sql_sources = Sources(self.profile)
        for _file, _name in find_files(self.profile.sources):
            log.info(">> %s", _file)
            _sql = sql_sources.render(template=_file)
            yield (_file, Job(name=_name, sql=_sql))
            self._write_sqls(name=_file, sql=_sql, root=target_dir)

    def _write_sqls(self, name: str, sql: str, root: str) -> None:
        """Write SQL files.

        Writes the SQL files to the specified directory.

        Args:
            name (str): The SQL file name.
            sql (str): The SQL content.
            root (str): The root directory to save the SQL files.
        """
        _file_path = path.join(root, name)
        Path(path.dirname(_file_path)).mkdir(parents=True, exist_ok=True)
        with open(file=_file_path, mode="w", encoding='utf-8') as _file:
            _file.write(sql)
            log.info("<< %s", _file_path)

    def create_workflows(self) -> Iterator[Workflow]:
        """Return the workflows as a JSON string.

        Creates and returns the workflows based on the read SQL jobs.
        """
        for _file, _job in self.jobs.items():
            log.debug("JOB[%s] -> %s", _job.name, _file)
            workflow =  Workflow(self, _job.name,
                                 repository=self.containers.repository,
                                 cmk=self.cmk,
                                 job=_job,
                                 file=_file)
            yield workflow
            # Adds dependencies between constructs.
            workflow.node.add_dependency(self.databases)
            workflow.node.add_dependency(self.containers)
