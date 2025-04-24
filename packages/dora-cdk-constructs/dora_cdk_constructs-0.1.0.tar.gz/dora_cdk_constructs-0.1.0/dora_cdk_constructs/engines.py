"""Dora Engine CDK constructs.

This module contains constructs for creating and managing AWS Lambda functions
integrated with Dora's data processing infrastructure.
"""

from os import environ
from constructs import Construct
from aws_cdk import (
    Aws,
    Size,
    Duration,
    aws_lambda as _lambda,
    aws_kms as kms,
    aws_iam as iam,
    aws_ecr as ecr,
    aws_lakeformation as lfm,
)

from dora_aws import __version__
from dora_aws.utils import s3_bucket_key
from dora_core.utils import logger
from dora_core.asset import Table

log = logger(__name__)

class Lambda(Construct):
    """Dora function construct class.

    This class encapsulates the creation and configuration of an AWS Lambda function,
    including permissions and environment settings.

    Attributes:
        table (Table): The Dora table associated with the Lambda function.
        cmk (kms.Key): The KMS key for encrypting environment variables.
        repository (ecr.Repository): The ECR repository containing the Lambda function's Docker image.
        function (_lambda.DockerImageFunction): The created Lambda function.
    """
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """Initialize the Lambda construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            construct_id (str): The ID of this construct.
            **kwargs: Additional keyword arguments, including 'table', 'cmk', and 'repository'.
        """
        super().__init__(scope, construct_id, **{})
        self.table:Table = kwargs["table"]
        self.cmk:kms.Key = kwargs["cmk"]
        self.repository:ecr.Repository = kwargs["repository"]
        # Create the Lambda function
        self.function = self.create_function()
        self.grants()

    def grants(self) -> None:
        """Grants the necessary permissions to the Lambda function.

        This method calls other methods to grant permissions for the ECR repository,
        IAM roles, KMS key, and LakeFormation.
        """
        self.grant_repo()
        self.grant_iam()
        self.grant_cmk()
        self.grant_lake()

    def grant_repo(self) -> None:
        """Grant the ECR repository permissions to the Lambda function.

        This method grants the Lambda function permission to pull images from the specified ECR repository.
        """
        self.repository.grant_pull(self.function)

    def grant_iam(self) -> None:
        """Grant the IAM permissions to the Lambda function.

        This method grants the Lambda function necessary IAM permissions to access S3, Glue, and Athena services.
        """
        # Grant to S3
        if self.table.location:
            self._grant_iam_s3(self.table.location)
        if self.table.source:
            self._grant_iam_s3(self.table.source)
        for _ref in self.table.ref_locations:
            self._grant_iam_s3(_ref)
        # Grant to AWS Glue
        self.function.add_to_role_policy(iam.PolicyStatement(
            resources=['*'], actions=["glue:*"]))
        # Grant to Amazon Athena
        self.function.add_to_role_policy(iam.PolicyStatement(
            resources=['*'], actions=["athena:*"]
        ))


    def _grant_iam_s3(self, s3_path:str) -> None:
        """Grants the S3 permissions to the Lambda function.

        Args:
            s3_path (str): The S3 path for which permissions are granted.

        This method grants the Lambda function permissions to access the specified S3 bucket and its contents.
        """
        _bkt, _pfx = s3_bucket_key(s3_path)
        _pfx_arn = '/'.join(_pfx.split('/')[:-1])
        _bkt_arn = f"arn:aws:s3:::{_bkt}"
        # Grants to s3 bucket
        self.function.add_to_role_policy(iam.PolicyStatement(
            resources=[_bkt_arn], actions=["s3:*"]
        ))
        # Grants to s3 files
        self.function.add_to_role_policy(iam.PolicyStatement(
            resources=[f"{_bkt_arn}/{_pfx_arn}/*"], actions=["s3:*"]
        ))

    def grant_cmk(self) -> None:
        """Grant the CMK key permissions to the Lambda function.

        This method grants the Lambda function permission to use the specified KMS key for encrypting and decrypting data.
        """
        self.cmk.grant_encrypt_decrypt(self.function.role)

    def grant_lake(self) -> None:
        """Grant the LakeFormation permissions to the Lambda function.

        This method grants the Lambda function necessary LakeFormation permissions to access the specified databases and tables.
        """
        # Grant permissions to the references
        for _ref in self.table.upstream_tables:
            if _ref.db != str() and _ref.name != str():
                lfm.CfnPermissions(
                    scope=self,
                    id=f"{self.table.name}-fn-lf-{_ref}",
                    data_lake_principal=lfm.CfnPermissions.DataLakePrincipalProperty(
                        data_lake_principal_identifier=self.function.role.role_arn
                    ),
                    resource=lfm.CfnPermissions.ResourceProperty(
                        database_resource=lfm.CfnPermissions.DatabaseResourceProperty(
                            catalog_id=Aws.ACCOUNT_ID,
                            name=str(_ref.db)
                        ),
                        table_resource=lfm.CfnPermissions.TableResourceProperty(
                            catalog_id=Aws.ACCOUNT_ID,
                            database_name=str(_ref.db),
                            name=str(_ref.name)
                        ),
                    ),
                    permissions=["ALL"],
                    permissions_with_grant_option=["ALL"]
                )
        # Grant permissions to the main table
        lfm.CfnPermissions(
            scope=self,
            id=f"{self.table.name}-fn-lf",
            data_lake_principal=lfm.CfnPermissions.DataLakePrincipalProperty(
                data_lake_principal_identifier=self.function.role.role_arn
            ),
            resource=lfm.CfnPermissions.ResourceProperty(
                database_resource=lfm.CfnPermissions.DatabaseResourceProperty(
                    catalog_id=Aws.ACCOUNT_ID,
                    name=self.table.database
                ),
                table_resource=lfm.CfnPermissions.TableResourceProperty(
                    catalog_id=Aws.ACCOUNT_ID,
                    database_name=self.table.database,
                    name=self.table.table
                ),
            ),
            permissions=["ALL"],
            permissions_with_grant_option=["ALL"]
        )

    def create_function(self) -> _lambda.DockerImageFunction:
        """Create the Lambda function.

        This method creates an AWS Lambda function using a Docker image from the specified ECR repository.

        Returns:
            _lambda.DockerImageFunction: The created Lambda function.
        """
        return _lambda.DockerImageFunction(
            scope=self,
            id=f"{self.table.name}-fn",
            memory_size=self.table.deployment_conf['memory'],
            ephemeral_storage_size=Size.mebibytes(self.table.deployment_conf['storage']),
            timeout=Duration.minutes(15),
            environment={
                "LOG_LEVEL": environ.get('LOG_LEVEL', 'DEBUG'),
                "MAX_MEMORY": str(self.table.deployment_conf['memory']),
            },
            # Docker Container image
            code=_lambda.DockerImageCode.from_ecr(
                repository=self.repository,
                tag_or_digest=__version__,
                cmd=["write.lambda_handler"]),
            environment_encryption=self.cmk)
