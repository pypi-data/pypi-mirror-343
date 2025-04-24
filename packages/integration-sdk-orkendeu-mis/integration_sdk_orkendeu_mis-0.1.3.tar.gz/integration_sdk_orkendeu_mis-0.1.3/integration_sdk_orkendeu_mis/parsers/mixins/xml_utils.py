from typing import Optional, Dict, Any, List, Union
from lxml import etree


class XMLUtilsMixin:
    """
    Миксин для работы с XML.
    """

    def parse_xml(self, data: bytes) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Парсит XML данные в словарь или список словарей.

        :param data: Данные в формате XML.
        :return: Распарсенные данные.
        """

        root = etree.fromstring(data)
        return self._xml_to_dict(root)

    def _xml_to_dict(self, element: etree.Element) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Преобразует элемент XML в словарь или список словарей.

        :param element: Элемент XML.
        :return: Словарь или список словарей.
        """

        if len(element) == 0:
            return element.text or ""

        result: Dict[str, Any] = {}
        for child in element:
            child_result = self._xml_to_dict(child)
            if child.tag in result:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_result)
            else:
                result[child.tag] = child_result

        return result

    def extract_text(self, root: etree.Element, tag: str) -> Optional[str]:
        """
        Извлекает текст из элемента XML по тегу.
        :param root: Корневой элемент XML.
        :param tag: Тег, из которого нужно извлечь текст.
        :return: Извлеченный текст или None, если тег не найден.
        """

        el = root.find(f".//{tag}")
        return el.text if el is not None else None

    def extract_all_texts(self, root: etree.Element, tag: str) -> List[str]:
        """
        Извлекает все тексты из элементов XML по тегу.
        :param root: Корневой элемент XML.
        :param tag: Тег, из которого нужно извлечь тексты.
        :return: Список извлеченных текстов.
        """

        return [el.text for el in root.findall(f".//{tag}") if el.text]