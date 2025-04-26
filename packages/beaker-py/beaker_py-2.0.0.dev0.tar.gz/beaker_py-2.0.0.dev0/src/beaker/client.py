from __future__ import annotations

import logging
import os
import time
from contextlib import contextmanager
from functools import cached_property
from typing import Generator, TypeVar

import grpc
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from . import beaker_pb2_grpc
from ._cluster import ClusterClient
from ._dataset import DatasetClient
from ._experiment import ExperimentClient
from ._group import GroupClient
from ._image import ImageClient
from ._job import JobClient
from ._node import NodeClient
from ._organization import OrganizationClient
from ._secret import SecretClient
from ._user import UserClient
from ._workload import WorkloadClient
from ._workspace import WorkspaceClient
from .config import Config, InternalConfig
from .exceptions import *
from .version import VERSION

__all__ = ["Beaker"]


_LATEST_VERSION_CHECKED = False
T = TypeVar("T")


class Beaker:
    """
    A client for interacting with `Beaker <https://beaker.org>`_.

    :param config: The Beaker :class:`Config`.
    :param check_for_upgrades: Automatically check that beaker-py is up-to-date. You'll see
        a warning if it isn't.
    :param user_agent: Override the "User-Agent" header used in requests to the Beaker server.
    """

    API_VERSION = "v3"
    CLIENT_VERSION = VERSION
    VERSION_CHECK_INTERVAL = 12 * 3600  # 12 hours

    RECOVERABLE_SERVER_ERROR_CODES = (429, 500, 502, 503, 504)
    MAX_RETRIES = 5
    BACKOFF_FACTOR = 1
    BACKOFF_MAX = 120
    TIMEOUT = 5.0
    POOL_MAXSIZE = min(100, (os.cpu_count() or 16) * 6)

    logger = logging.getLogger("beaker")

    def __init__(
        self,
        config: Config,
        check_for_upgrades: bool = True,
        user_agent: str = f"beaker-py v{VERSION}",
    ):
        self.user_agent = user_agent
        self._config = config
        self._channel: grpc.Channel | None = None
        self._service: beaker_pb2_grpc.BeakerStub | None = None
        self._http_session: requests.Session | None = None

        # See if there's a newer version, and if so, suggest that the user upgrades.
        if check_for_upgrades:
            self._check_for_upgrades()

    def _check_for_upgrades(self):
        global _LATEST_VERSION_CHECKED

        if _LATEST_VERSION_CHECKED:
            return

        import warnings

        import packaging.version
        import requests

        try:
            config = InternalConfig.load()
            if (
                config is not None
                and config.version_checked is not None
                and (time.time() - config.version_checked <= self.VERSION_CHECK_INTERVAL)
            ):
                return

            # TODO: update URL
            response = requests.get(
                "https://api.github.com/repos/allenai/beaker-py/releases/latest", timeout=1
            )
            if response.ok:
                latest_version = packaging.version.parse(response.json()["tag_name"])
                if latest_version > packaging.version.parse(self.CLIENT_VERSION):
                    warnings.warn(
                        f"You're using beaker-py v{self.CLIENT_VERSION}, "
                        f"but a newer version (v{latest_version}) is available.\n\n"
                        f"Please upgrade with `pip install --upgrade beaker-py`.\n\n"
                        f"You can find the release notes for v{latest_version} at "
                        f"https://github.com/allenai/beaker-py/releases/tag/v{latest_version}\n",
                        UserWarning,
                    )

                _LATEST_VERSION_CHECKED = True
                if config is not None:
                    config.version_checked = time.time()
                    config.save()
        except Exception:
            pass

    @classmethod
    def from_env(
        cls,
        check_for_upgrades: bool = True,
        user_agent: str = f"beaker-py v{VERSION}",
        **overrides,
    ) -> Beaker:
        """
        Initialize client from a config file and/or environment variables.

        :param check_for_upgrades: Automatically check that beaker-py is up-to-date. You'll see
            a warning if it isn't.
        :param user_agent: Override the "User-Agent" header used in requests to the Beaker server.
        :param overrides: Fields in the :class:`Config` to override.

        .. note::
            This will use the same config file that the `Beaker command-line client
            creates and uses, which is usually located at ``$HOME/.beaker/config.yml``.

            If you haven't configured the command-line client, then you can alternately just
            set the environment variable ``BEAKER_TOKEN`` to your Beaker `user token <https://beaker.org/user>`_.

        """
        return cls(
            Config.from_env(**overrides),
            check_for_upgrades=check_for_upgrades,
            user_agent=user_agent,
        )

    @property
    def service(self) -> beaker_pb2_grpc.BeakerStub:
        if self._service is None:
            self._channel = grpc.secure_channel(
                self.config.rpc_address, grpc.ssl_channel_credentials()
            )
            self._service = beaker_pb2_grpc.BeakerStub(self._channel)
        return self._service

    @property
    def config(self) -> Config:
        """
        The client's :class:`Config`.
        """
        return self._config

    @cached_property
    def user_name(self) -> str:
        return self.user.get().name

    @cached_property
    def org_name(self) -> str:
        return self.organization.get().name

    @cached_property
    def organization(self) -> OrganizationClient:
        """
        Manage organizations.
        """
        return OrganizationClient(self)

    @cached_property
    def user(self) -> UserClient:
        """
        Manage users.
        """
        return UserClient(self)

    @cached_property
    def workspace(self) -> WorkspaceClient:
        """
        Manage workspaces.
        """
        return WorkspaceClient(self)

    @cached_property
    def cluster(self) -> ClusterClient:
        """
        Manage clusters.
        """
        return ClusterClient(self)

    @cached_property
    def node(self) -> NodeClient:
        """
        Manage nodes.
        """
        return NodeClient(self)

    @cached_property
    def dataset(self) -> DatasetClient:
        """
        Manage datasets.
        """
        return DatasetClient(self)

    @cached_property
    def image(self) -> ImageClient:
        """
        Manage images.
        """
        return ImageClient(self)

    @cached_property
    def job(self) -> JobClient:
        """
        Manage jobs.
        """
        return JobClient(self)

    @cached_property
    def experiment(self) -> ExperimentClient:
        """
        Manage experiments.
        """
        return ExperimentClient(self)

    @cached_property
    def workload(self) -> WorkloadClient:
        """
        Manage workloads.
        """
        return WorkloadClient(self)

    @cached_property
    def secret(self) -> SecretClient:
        """
        Manage secrets.
        """
        return SecretClient(self)

    @cached_property
    def group(self) -> GroupClient:
        """
        Manage groups.
        """
        return GroupClient(self)

    @contextmanager
    def http_session(self) -> Generator[requests.Session, None, None]:
        if self._http_session is None:
            session = requests.Session()
            retries = Retry(
                total=self.MAX_RETRIES * 2,
                connect=self.MAX_RETRIES,
                status=self.MAX_RETRIES,
                backoff_factor=self.BACKOFF_FACTOR,
                status_forcelist=self.RECOVERABLE_SERVER_ERROR_CODES,
            )
            session.mount(
                "https://", HTTPAdapter(max_retries=retries, pool_maxsize=self.POOL_MAXSIZE)
            )
            self._http_session = session
            try:
                yield self._http_session
            finally:
                self._http_session.close()
                self._http_session = None
        else:
            yield self._http_session

    def __enter__(self) -> "Beaker":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del exc_type, exc_val, exc_tb
        self.close()
        return False

    def close(self):
        if self._channel is not None:
            self._channel.close()
        self._channel = None
        self._service = None
        if self._http_session is not None:
            self._http_session.close()
        self._http_session = None

    def __del__(self):
        self.close()
