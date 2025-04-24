# -*- coding: utf-8 -*-
"""Dora Catalog CDK constructs.

This module contains constructs for creating and managing Dora containers and databases using AWS CDK.
"""
from typing import Iterator, List
from aws_cdk import (
    Aws,
    RemovalPolicy,
    aws_ecr as ecr,
    aws_glue as glue
)
from constructs import Construct
import cdk_ecr_deployment as ecrdeploy

from dora_core import __version__
from dora_core.utils import logger
from dora_core.asset import Job

log = logger(__name__)

class Containers(Construct):
    """Dora containers construct class.

    This construct sets up an ECR repository and deploys a Docker image to it.

    Attributes:
        repository (ecr.Repository): The ECR repository for the container.
        image (ecrdeploy.ECRDeployment): The deployment of the Docker image to the ECR repository.
    """
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """
        Initialize the Containers construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            construct_id (str): The ID of this construct.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(scope, construct_id, **{})
        _name = kwargs.get("name", "dora")
        _uri = f"{Aws.ACCOUNT_ID}.dkr.ecr.{Aws.REGION}.amazonaws.com/{_name}:{__version__}"
        self.repository = ecr.Repository(
            scope=self,
            id="repository",
            empty_on_delete=True,
            removal_policy=RemovalPolicy.DESTROY,
            repository_name=_name)
        self.image = ecrdeploy.ECRDeployment(self, "container-engine",
            src=ecrdeploy.DockerImageName(f"doraimg/duckdb:{__version__}"),
            dest=ecrdeploy.DockerImageName(_uri))
        # # Copy from docker registry to ECR.
        self.image.node.add_dependency(self.repository)

class Databases(Construct):
    """Dora databases construct class.

    This construct creates Glue databases based on the provided jobs.

    Attributes:
        databases (List[glue.CfnDatabase]): A list of Glue databases created.
    """
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """
        Initialize the Databases construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            construct_id (str): The ID of this construct.
            **kwargs: Additional keyword arguments, including 'jobs' which is a list of Job objects.
        """
        super().__init__(scope, construct_id, **{})
        self.databases = list(self.create_databases(kwargs["jobs"]))

    def create_databases(self, jobs: List[Job]) -> Iterator[glue.CfnDatabase]:
        """Create databases.

        This method iterates over the provided jobs and creates Glue databases for each unique database name found.

        Args:
            jobs (List[Job]): A list of Job objects containing table information.

        Yields:
            glue.CfnDatabase: A Glue database construct.
        """
        _dbs = list()
        for _job in jobs.values():
            for _table in _job.tables:
                if _table.database not in _dbs:
                    _dbs.append(_table.database)
        for _db in _dbs:
            log.debug("DATABASE[%s]", _db)
            yield glue.CfnDatabase(
                scope=self,
                id=f"glue:database:{_db}",
                catalog_id=Aws.ACCOUNT_ID,
                database_input=glue.CfnDatabase.DatabaseInputProperty(name=_db))
