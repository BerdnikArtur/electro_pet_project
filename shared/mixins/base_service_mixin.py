from ..exceptions import MissingRepositoryError
from core.infrastructure.repositories.base_repository import BaseRepository
from ..base_service import BaseService

from typing import Type, Dict
import logging

logger = logging.getLogger(__name__)

class BaseViewMixin:
    service_class: Type[BaseService] = None
    repository_classes: Dict[str, Type[BaseRepository]] = {}

    @property
    def service(self):
        if self.service_class is None:
            logger.warning(f"{self.__class__.__name__}: View should define his own service")
            return None
        if not hasattr(self, "_service_instance") and not hasattr(self, "_repository_instances"):
            if not self.repository_classes:
                logger.warning(f"{self.__class__.__name__}: View should define his own repository")
            
            self._repository_instances = {}
            for name, repo_class in self.repository_classes.items():
                if issubclass(repo_class, BaseRepository):
                    self._repository_instances[name] = repo_class()
                else:
                    raise MissingRepositoryError(message=f"{self.__class__.__name__}: Repository '{name}' is not defined")
                

            self._service_instance = self.service_class(**self._repository_instances)
        return self._service_instance