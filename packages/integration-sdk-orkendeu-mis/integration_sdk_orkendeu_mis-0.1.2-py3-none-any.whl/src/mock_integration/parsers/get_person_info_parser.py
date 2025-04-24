import json

from abc import ABC
from typing import Union

from integration_sdk_orkendeu_mis.parsers.abstract import AbstractParser
from integration_sdk_orkendeu_mis.parsers.mixins.error_check import ServiceUnavailableError, SubjectNotFoundError


class GetPersonInfoMockParser(AbstractParser, ABC):
    def parse(self, data_to_parse: bytes) -> Union[dict, list]:
        if not data_to_parse:
            raise ServiceUnavailableError("Empty mock response")

        result = json.loads(data_to_parse)

        if "error" in result:
            raise SubjectNotFoundError(result["error"])

        return result