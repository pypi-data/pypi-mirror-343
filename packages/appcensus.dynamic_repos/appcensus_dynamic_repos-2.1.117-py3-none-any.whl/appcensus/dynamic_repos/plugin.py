import logging
from typing import List
from typing import Type

from cleo.io.io import IO
from poetry.console.application import Application
from poetry.console.commands.command import Command
from poetry.factory import Factory
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry
from poetry.utils.password_manager import PasswordManager

from appcensus.dynamic_repos import REPO_FILE_PATH
from appcensus.dynamic_repos.auth import CredentialCache
from appcensus.dynamic_repos.auth import CredentialManager
from appcensus.dynamic_repos.commands import RepoClearCredentials
from appcensus.dynamic_repos.commands import RepoDisableCommand
from appcensus.dynamic_repos.commands import RepoEnableCommand
from appcensus.dynamic_repos.commands import RepoSetAuth
from appcensus.dynamic_repos.commands import RepoShowCommand
from appcensus.dynamic_repos.commands import RepoShowCredentials
from appcensus.dynamic_repos.commands import RepoUseCommand
from appcensus.dynamic_repos.models import Repo
from appcensus.dynamic_repos.models import RepoManager
from appcensus.dynamic_repos.pool_manager import PoolManager
from appcensus.dynamic_repos.repo_collector import RepoCollector

logger = logging.getLogger(__name__)


class DynamicRepos(Plugin):
    _create_pool = Factory.create_pool

    def _check_repo(self, existing_repos: List[Repo], new_repo: Repo) -> bool:
        for repo in existing_repos:
            if repo == new_repo:
                raise ValueError(
                    f"Identical source <c1>{new_repo.name}</> already exists. Perhaps you have a declaration in"
                    " pyproject.toml. You should resolve the redundancy to prevent conflict."
                )

            if repo.name == new_repo.name:
                raise ValueError(
                    f"Inconsistent source with name <c1>{new_repo.name}</c1> already exists."
                    " Please reconile this."
                )

        return True

    def _configure_repositories(self, poetry: Poetry, io: IO) -> None:
        logger.debug("Configuring repositories ...")

        existing_repos = RepoCollector(poetry.pool).repositories()

        logger.debug(f"Beginning with {len(existing_repos)} existing repositories")
        for repo in existing_repos:
            logger.debug(f"- {repo}")

        new_repositories: List[Repo] = []

        for name in RepoManager.entries():
            repo = RepoManager.get(name)
            if repo.enabled:
                try:
                    if self._check_repo(existing_repos, repo):
                        if repo.auth:
                            try:
                                logger.debug(f"Authorizing repo {repo.name} ...")
                                pm = PasswordManager(poetry.config)
                                CredentialManager.authorize(pm, repo)
                            finally:
                                CredentialCache.save()

                        logger.debug(f"Adding {repo.name}")
                        new_repositories.append(repo)
                except Exception as e:
                    self._exceptional_error(io, e)
                    return

        # configure new sources
        logger.debug(f"Configuring {len(new_repositories)} sources ...")
        PoolManager(poetry, io).create_pool(new_repositories)

    def _exceptional_error(self, io: IO, e: Exception) -> None:
        logger.error(e, exc_info=True)
        io.write_error_line(f"DynamicRepos: <error>{e}</error>")

    def activate(self, poetry: Poetry, io: IO) -> None:
        logger.debug("Activating appcensus.dynamic_repos")
        if not REPO_FILE_PATH.exists():
            return
        self._configure_repositories(poetry, io)


class DynamicReposApplication(ApplicationPlugin):
    @property
    def commands(self) -> List[Type[Command]]:
        return [
            RepoShowCommand,
            RepoEnableCommand,
            RepoDisableCommand,
            RepoSetAuth,
            RepoShowCredentials,
            RepoClearCredentials,
            RepoUseCommand,
        ]

    def activate(self, application: Application) -> None:
        for command in self.commands:
            assert command.name
            application.command_loader.register_factory(command.name, command)
