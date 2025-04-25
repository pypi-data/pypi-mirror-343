import logging
from typing import List

from cleo.io.io import IO
from poetry.factory import Factory
from poetry.poetry import Poetry
from poetry.repositories.repository_pool import RepositoryPool

from appcensus.dynamic_repos.models import Repo

logger = logging.getLogger(__name__)


# PoolManager creates new repositories via the poetry Factory and adds them to the pool.
class PoolManager:
    _poetry: Poetry
    _pool: RepositoryPool
    _io: IO | None

    def __init__(self, poetry: Poetry, io: IO | None) -> None:
        self._poetry = poetry
        self._pool = poetry.pool
        self._io = io

    def create_pool(self, repos: List[Repo]) -> None:
        self._poetry.set_pool(
            Factory.create_pool(
                self._poetry.config, [repo.to_source_dict() for repo in repos], self._io
            )
        )
