from __future__ import annotations

import ultima_scraper_api
from ultima_scraper_api.apis import api_helper
from ultima_scraper_api.apis.fansly import classes as fansly_classes
from ultima_scraper_api.apis.onlyfans import classes as onlyfans_classes
from ultima_scraper_api.classes.make_settings import Config

auth_types = (
    onlyfans_classes.auth_model.create_auth | fansly_classes.auth_model.create_auth
)
user_types = (
    onlyfans_classes.user_model.create_user | fansly_classes.user_model.create_user
)
error_types = onlyfans_classes.extras.ErrorDetails | fansly_classes.extras.ErrorDetails
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    api_types = ultima_scraper_api.api_types


class StreamlinedAPI:
    def __init__(
        self,
        api: api_types,
        config: Config,
    ) -> None:
        from ultima_scraper_api.managers.job_manager.job_manager import JobManager

        self.api = api
        self.max_threads = config.settings.max_threads
        self.config = config
        self.lists = None
        self.pool = api_helper.CustomPool()

        self.job_manager = JobManager()

    def has_active_auths(self):
        return bool([x for x in self.api.auths if x.active])

    def get_auths_via_subscription_identifier(self, identifier: str):
        for auth in self.api.auths:
            if auth.username == identifier:
                pass

    def get_site_settings(self):
        return self.config.supported.get_settings(self.api.site_name)

    def get_global_settings(self):
        return self.config.settings

    async def close_pools(self):
        for auth in self.api.auths:
            await auth.session_manager.active_session.close()
