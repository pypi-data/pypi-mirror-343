"""
LoaderManager - Orchestrates loading multiple resources with strategies, concurrency, filtering, aggregation.
"""

from python.loader.executor import Executor
from python.loader.aggregator import Aggregator
from python.loader.normalizer import ResourceNormalizer
from python.loader.strategies.http_loader import HTTPLoader
from python.loader.strategies.s3_loader import S3Loader
from python.loader.strategies.gcs_loader import GCSLoader
from python.loader.strategies.azure_loader import AzureLoader
from python.loader.strategies.file_path_loader import FilePathLoader
from python.loader.strategies.data_url_loader import DataURLLoader

class LoaderManager:
    """
    Loader manager that combines strategy selection, execution, filtering, and aggregation.
    """

    def __init__(self, resource_agent=None, timeout=10, max_concurrent=5, multithreading=True, multiprocessing=False):
        """
        Initialize LoaderManager.

        Args:
            resource_agent (dict): Resource agents (e.g., {"s3": boto3, "gs": GCP Client})
            timeout (int): HTTP timeout seconds
            max_concurrent (int): Max concurrent workers
            multithreading (bool): Use threading if True
            multiprocessing (bool): Use multiprocessing if True
        """
        self.resource_agent = resource_agent or {}
        self.timeout = timeout
        self.executor = Executor(max_concurrent=max_concurrent, multithreading=multithreading, multiprocessing=multiprocessing)
        self.strategies = [
            HTTPLoader(),
            S3Loader(),
            GCSLoader(),
            AzureLoader(),
            FilePathLoader(),
            DataURLLoader(),
        ]

    def load(self, text=None, path=None, uri=None, resources=None,
             mode="merge", filter_func=None, root_keys=None,
             error_policy="fail-fast", stream_mode="memory", **opts):
        """
        Main load function.

        Args:
            text, path, uri: Single inputs
            resources: List of resources (paths, uris, or mixed)
            mode: Aggregation mode ('merge', 'list', 'groupby:key')
            filter_func: Optional filter function
            root_keys: Optional root keys to extract
            error_policy: 'fail-fast' or 'skip'
            stream_mode: 'memory' or 'streaming'
            **opts: Additional options

        Returns:
            Aggregated result
        """
        if resources is None:
            resources = []
            if uri:
                resources.append(uri)
            if path:
                resources.append(path)
            if text:
                resources.append(text)

        normalizer = ResourceNormalizer(self.resource_agent)
        normalized_resources = normalizer.normalize(resources)

        tasks = [lambda entry=entry: self._load_one(entry, stream_mode=stream_mode, **opts) for entry in normalized_resources]

        results = self.executor.submit_all(tasks)

        parsed = []
        for result in results:
            if isinstance(result, Exception):
                if error_policy == "fail-fast":
                    raise result
                elif error_policy == "skip":
                    continue
            else:
                parsed.append(result)

        if filter_func:
            parsed = list(filter(filter_func, parsed))

        if root_keys:
            parsed = [self._extract_roots(p, root_keys) for p in parsed]

        aggregator = Aggregator(mode)
        return aggregator.aggregate(parsed)

    def _load_one(self, entry, stream_mode="memory", **opts):
        resource = entry["resource"]
        agent_name = entry.get("agent")
        agent_object = entry.get("agent_object")

        for strategy in self.strategies:
            if strategy.can_load(resource):
                agent = agent_object
                if not agent and agent_name:
                    agent = self.resource_agent.get(agent_name)
                if not agent and isinstance(strategy, S3Loader):
                    agent = self.resource_agent.get("s3")
                elif not agent and isinstance(strategy, GCSLoader):
                    agent = self.resource_agent.get("gs")
                elif not agent and isinstance(strategy, AzureLoader):
                    agent = self.resource_agent.get("azure")

                return strategy.load(resource, resource_agent=agent, stream_mode=stream_mode, timeout=self.timeout, **opts)

        raise ValueError(f"[LoaderManager] No strategy found for resource: {resource}")

    def _extract_roots(self, data, root_keys):
        if isinstance(data, dict):
            return {k: v for k, v in data.items() if k in root_keys}
        return data
