from abc import ABC
from typing import Optional, List

from integration_sdk_orkendeu_mis.data_subjects.schema import ParamSchema


class AbstractProvider(ABC):
    """
    Абстрактный класс для всех классов, которые будут использоваться в качестве Provider.
    """

    code: str
    label: str
    description: Optional[str] = ""
    params: List[ParamSchema] = []

    def get_param_by_name(self, name: str) -> Optional[ParamSchema] | None:
        """
        Возвращает параметр по имени.
        :param name: Имя параметра.
        :return: Параметр или None, если параметр не найден.
        """

        return next((param for param in self.params if param.name == name), None)

    def get_all_required_params(self) -> List[ParamSchema]:
        """
        Возвращает все обязательные параметры.
        :return: Список обязательных параметров.
        """

        return [param for param in self.params if param.required]
