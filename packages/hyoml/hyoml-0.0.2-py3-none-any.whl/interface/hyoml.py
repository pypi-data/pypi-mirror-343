"""
Hyoml unified orchestrator class with output support for saving to files, URIs, or cloud storage (via passed agents).
"""

from python.parser.core.hyoml_parser import HyomlParser
from python.parser.core.factory import FormatterFactory
from utils.validator import Validator
from python.parser.core.manipulation.sorter import DataSorter
from python.parser.core.manipulation.searcher import DataSearcher

from interface.helpers.format_helpers import FormatHelper
from interface.helpers.validation_helpers import ValidationHelper
from interface.helpers.aliases import AliasHelper

from python.loader.loader_manager import LoaderManager
import os
import requests
from utils.conversion_utils import dict_to_list, dict_to_tuple  # Importing conversion utilities
from python.cloud_storage.cloud_storage_agent import CloudStorageAgent  # Import the base CloudStorageAgent class

class Hyoml:
    """
    Unified interface for parsing, formatting, validating, sorting, and searching Hyoml data.
    Now supports multiple resource loading via LoaderManager and strict profiles.
    """

    def __init__(self, options=None, strict_file=None, strict_uri=None, strict_text=None):
        self.options = options or {}
        self.strict_rules = {}

        # Load strict rules if provided
        try:
            strict_content = None

            if strict_file:
                if not os.path.isfile(strict_file):
                    raise FileNotFoundError(f"Strict file not found: {strict_file}")
                with open(strict_file, "r", encoding="utf-8") as f:
                    strict_content = f.read()

            elif strict_uri:
                response = requests.get(strict_uri)
                response.raise_for_status()
                strict_content = response.text

            elif strict_text:
                strict_content = strict_text

            if strict_content:
                parser = HyomlParser()
                parsed_strict = parser.parse(strict_content)
                self.options.update(parsed_strict)

        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[Hyoml.__init__] Failed to load strict rules: {e}")

        self.parser = HyomlParser(options=self.options)
        self.formatter_factory = FormatterFactory()
        self.validator = Validator()
        self.sorter = DataSorter()
        self.searcher = DataSearcher()

        # Helpers (composition)
        self.format_helper = FormatHelper(self)
        self.validation_helper = ValidationHelper(self)
        self.alias_helper = AliasHelper(self)

    def parse(self, text=None, path=None, uri=None, resources=None,
              resource_agent=None, mode="merge", filter_func=None, root_keys=None,
              error_policy="fail-fast", stream_mode="memory", **opts):
        try:
            loader = LoaderManager(
                resource_agent=resource_agent,
                timeout=self.options.get("timeout", 10),
                max_concurrent=self.options.get("max_concurrent", 5),
                multithreading=self.options.get("multithreading", True),
                multiprocessing=self.options.get("multiprocessing", False)
            )

            loaded = loader.load(
                text=text, path=path, uri=uri, resources=resources,
                mode=mode, filter_func=filter_func, root_keys=root_keys,
                error_policy=error_policy, stream_mode=stream_mode, **opts
            )

            if isinstance(loaded, str):
                return self.parser.parse(loaded)
            elif isinstance(loaded, dict) or isinstance(loaded, list):
                return loaded
            else:
                raise ValueError("[Hyoml.parse] Unsupported loaded data type")

        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[Hyoml.parse] Failed: {e}")

    # Aliases for parse
    load = loads = decode = deserialize = read = parse

    def format(self, data, fmt, path=None, cloud_agent: CloudStorageAgent = None, **opts):
        try:
            formatter = self.formatter_factory.create(fmt)
            if not formatter:
                raise ValueError(f"[Hyoml.format] Unknown formatter type: {fmt}")
            output = formatter.format(data, **opts)

            # Handle saving output to a file, URI, or cloud storage
            if path:
                if self._is_uri(path):
                    # Upload to URI (e.g., HTTP endpoint)
                    self._upload_to_uri(output, path)
                elif self._is_cloud_storage(path):
                    # Upload to cloud (AWS, GCP, Azure) using the passed agent
                    if cloud_agent is None:
                        raise ValueError("[Hyoml.format] Cloud agent must be provided for cloud upload.")
                    self._upload_to_cloud(output, path, cloud_agent)
                else:
                    # Save to local file
                    self._save_to_local_file(output, path)
            return output
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[Hyoml.format] Failed: {e}")

    # Aliases for format
    stringify = dump = dumps = show = encode = serialize = output = format

    def validate(self, data, fmt):
        try:
            method = f"isValid{fmt.capitalize()}"
            if not hasattr(self.validator, method):
                raise ValueError(f"[Hyoml.validate] No validator found for format: {fmt}")
            return getattr(self.validator, method)(data)
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[Hyoml.validate] Failed: {e}")

    def sort(self, data, by="key", reverse=False, list_key=None):
        try:
            if isinstance(data, dict):
                if by == "key":
                    return self.sorter.sort_dict_by_keys(data, reverse)
                elif by == "value":
                    return self.sorter.sort_dict_by_values(data, reverse)
                else:
                    raise ValueError("Invalid sort 'by' for dict")
            elif isinstance(data, list) and list_key:
                return self.sorter.sort_list_of_dicts(data, list_key, reverse)
            else:
                raise ValueError("Unsupported sort format or missing list_key")
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[Hyoml.sort] Failed: {e}")

    def search(self, data, key=None, value=None):
        try:
            if key:
                return self.searcher.find_key(data, key)
            elif value is not None:
                return self.searcher.find_value(data, value)
            else:
                raise ValueError("Specify key or value to search")
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[Hyoml.search] Failed: {e}")

    # Dynamic format helpers, validation helpers, and alias helpers
    def __getattr__(self, name):
        if hasattr(self.format_helper, name):
            return getattr(self.format_helper, name)
        if hasattr(self.validation_helper, name):
            return getattr(self.validation_helper, name)
        if hasattr(self.alias_helper, name):
            return getattr(self.alias_helper, name)
        raise AttributeError(f"'Hyoml' object has no attribute '{name}'")

    # Utility Conversion Methods (using helper functions)
    
    def toDict(self, data):
        """
        Convert the data to a dictionary.
        
        Args:
            data (dict, list, tuple): The data to convert.

        Returns:
            dict: The converted data as a dictionary.
        """
        return dict_to_dict(data)
    
    def toList(self, data):
        """
        Convert the data to a list.
        
        Args:
            data (dict, list, tuple): The data to convert.

        Returns:
            list: The converted data as a list.
        """
        return dict_to_list(data)
    
    def toTuple(self, data):
        """
        Convert the data to a tuple.
        
        Args:
            data (dict, list, tuple): The data to convert.

        Returns:
            tuple: The converted data as a tuple.
        """
        return dict_to_tuple(data)

    # Private Helper Methods for Handling URI and Cloud Storage
    def _is_uri(self, path):
        """Check if the path is a URI (e.g., starts with 'http://', 'https://', etc.)."""
        return path.startswith("http://") or path.startswith("https://")

    def _is_cloud_storage(self, path):
        """Check if the path refers to cloud storage (AWS, GCP, Azure)."""
        return path.startswith("gs://") or path.startswith("s3://") or path.startswith("azure://")

    def _upload_to_uri(self, data, uri):
        """Upload data to a URI (e.g., HTTP endpoint)."""
        response = requests.post(uri, data=data)
        if response.status_code != 200:
            raise ValueError(f"[Hyoml._upload_to_uri] Failed to upload to URI: {uri}")
        return response

    def _upload_to_cloud(self, data, path, cloud_agent: CloudStorageAgent):
        """Upload data to cloud storage using the provided cloud agent."""
        cloud_agent.upload(data, path)

    def _save_to_local_file(self, data, path):
        """Save output to a local file."""
        with open(path, 'w', encoding='utf-8') as file:
            file.write(data)
