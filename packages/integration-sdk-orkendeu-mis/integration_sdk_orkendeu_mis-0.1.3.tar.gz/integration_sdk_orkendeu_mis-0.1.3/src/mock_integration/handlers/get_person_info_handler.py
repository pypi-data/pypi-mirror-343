from integration_sdk_orkendeu_mis.handlers.abstract import AbstractServiceHandler
from src.mock_integration.data_subjects.get_person_info_subject import GetPersonInfoMockSubject
from src.mock_integration.fetchers.get_person_info_fetcher import GetPersonInfoMockFetcher
from src.mock_integration.parsers.get_person_info_parser import GetPersonInfoMockParser


class GetPersonInfoMockHandler(AbstractServiceHandler):
    fetcher_class = GetPersonInfoMockFetcher
    parser_class = GetPersonInfoMockParser
    provider_class = GetPersonInfoMockParser
    data_subject_class = GetPersonInfoMockSubject
