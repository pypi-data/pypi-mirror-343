from .client import set_default_params
from .global_api.aio import ImplyPolarisGlobalClient
from .project_api.aio import ImplyPolarisProjectClient
from .regional_api.aio import ImplyPolarisRegionalClient


class ProjectClient(ImplyPolarisProjectClient):  # type: ignore
    """The Official Imply Polaris Project API Python SDK"""

    def __init__(
        self,
        project_id: str,
        domain: str,
        region: str,
        cloud_provider: str,
        api_key: str,
        **kwargs,
    ):
        """Instantiates a new client using OrgName, Region and CloudProvider

        .. code-block:: python
            domain = "imply"
            region = "us-east-1"
            cloud_provider = "aws"
            api_key = os.getenv("POLARIS_API_KEY")
            project_id = "4bd7330d-cb6d-489b-aa7b-22653f237f9d"
            client = ProjectClient(project_id, domain, region, cloud_provider, api_key)
        """
        set_default_params(api_key, kwargs)
        endpoint = f"https://{domain}.{region}.{cloud_provider}.api.imply.io"
        super().__init__(
            project_id=project_id, endpoint=endpoint, credential=api_key, **kwargs
        )

    @classmethod
    def from_endpoint(cls, project_id: str, endpoint: str, api_key: str, **kwargs):
        """Instantiates a new client using an endpoint url.

        .. code-block:: python
            api_key = os.getenv("POLARIS_API_KEY")
            project_id = "4bd7330d-cb6d-489b-aa7b-22653f237f9d"
            endpoint = "https://imply.us-east-1.aws.api.imply.io"
            client = ProjectClient.from_endpoint(project_id, endpoint, api_key)
        """
        set_default_params(api_key, kwargs)
        obj = cls.__new__(cls)  # Does not call __init__
        super(ProjectClient, obj).__init__(
            project_id=project_id, endpoint=endpoint, credential=api_key, **kwargs
        )
        return obj


class RegionalClient(ImplyPolarisRegionalClient):  # type: ignore
    """The Official Imply Polaris Regional API Python SDK"""

    def __init__(
        self,
        domain: str,
        region: str,
        cloud_provider: str,
        api_key: str,
        **kwargs,
    ):
        """Instantiates a new client using OrgName, Region and CloudProvider

        .. code-block:: python
            domain = "imply"
            region = "us-east-1"
            cloud_provider = "aws"
            api_key = os.getenv("POLARIS_API_KEY")
            client = RegionalClient(domain, region, cloud_provider, api_key)
        """
        set_default_params(api_key, kwargs)
        endpoint = f"https://{domain}.{region}.{cloud_provider}.api.imply.io"
        super().__init__(endpoint=endpoint, credential=api_key, **kwargs)

    @classmethod
    def from_endpoint(cls, endpoint: str, api_key: str, **kwargs):
        """Instantiates a new client using an endpoint url.

        .. code-block:: python
            api_key = os.getenv("POLARIS_API_KEY")
            endpoint = "https://imply.us-east-1.aws.api.imply.io"
            client = RegionalClient.from_endpoint(endpoint, api_key)
        """
        set_default_params(api_key, kwargs)
        obj = cls.__new__(cls)  # Does not call __init__
        super(RegionalClient, obj).__init__(
            endpoint=endpoint, credential=api_key, **kwargs
        )
        return obj


class GlobalClient(ImplyPolarisGlobalClient):  # type: ignore
    """The Official Imply Polaris Global API Python SDK"""

    def __init__(
        self,
        domain: str,
        api_key: str,
        **kwargs,
    ):
        """Instantiates a new client using OrgName, Region and CloudProvider

        .. code-block:: python
            api_key = os.getenv("POLARIS_API_KEY")
            domain = "imply"
            client = GlobalClient(domain, api_key)
        """
        set_default_params(api_key, kwargs)
        endpoint = f"https://{domain}.api.imply.io"
        super().__init__(endpoint=endpoint, credential=api_key, **kwargs)

    @classmethod
    def from_endpoint(cls, endpoint: str, api_key: str, **kwargs):
        """Instantiates a new client using an endpoint url.

        .. code-block:: python
            api_key = os.getenv("POLARIS_API_KEY")
            endpoint = "https://imply.api.imply.io"
            client = GlobalClient.from_endpoint(endpoint, api_key)
        """
        set_default_params(api_key, kwargs)
        obj = cls.__new__(cls)  # Does not call __init__
        super(GlobalClient, obj).__init__(
            endpoint=endpoint, credential=api_key, **kwargs
        )
        return obj
