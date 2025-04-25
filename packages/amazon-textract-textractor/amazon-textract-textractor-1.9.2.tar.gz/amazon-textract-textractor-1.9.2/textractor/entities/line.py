"""
Represents a single :class:`Line` Entity within the :class:`Document`. 
The Textract API response returns groups of words as LINE BlockTypes. They contain :class:`Word` entities as children. 

This class contains the associated metadata with the :class:`Line` entity including the entity ID, 
bounding box information, child words, page number, Page ID and confidence of detection.
"""

import logging
from typing import List

from textractor.entities.word import Word
from textractor.data.constants import TextTypes
from textractor.entities.bbox import BoundingBox
from textractor.exceptions import InputError
from textractor.entities.document_entity import DocumentEntity
from textractor.visualizers.entitylist import EntityList
from textractor.utils.html_utils import escape_text
from textractor.data.text_linearization_config import TextLinearizationConfig

class Line(DocumentEntity):
    """
    To create a new :class:`Line` object we need the following:

    :param entity_id: Unique identifier of the Line entity.
    :type entity_id: str
    :param bbox: Bounding box of the line entity.
    :type bbox: BoundingBox
    :param words: List of the Word entities present in the line
    :type words: list, optional
    :param confidence: confidence with which the entity was detected.
    :type confidence: float, optional
    """

    def __init__(
        self,
        entity_id: str,
        bbox: BoundingBox,
        words: List[Word] = None,
        confidence: float = 0,
    ):
        super().__init__(entity_id, bbox)
        if words is not None and len(words) > 0:
            self._children: List[Word] = sorted(words, key=lambda x: (x.bbox.x, x.bbox.y))
        else:
            self._children = []

        self._confidence = confidence / 100
        self._page = None
        self._page_id = None

    @property
    def text(self):
        """
        :return: Returns the text transcription of the :class:`Line` entity.
        :rtype: str
        """
        return " ".join([word.text for word in self.words])

    @property
    def words(self):
        """
        :return: Returns the line's children
        :rtype: List[Word]
        """
        return self._children

    def get_text_and_words(self, config: TextLinearizationConfig = TextLinearizationConfig()):
        if not self.bbox:
            self.bbox = BoundingBox.enclosing_bbox(self.words)
        for w in self.words:
            w.line_id = self.id
            w.line_bbox = self.bbox
        return escape_text(self.text, config), self.words

    @property
    def page(self):
        """
        :return: Returns the page number of the page the :class:`Line` entity is present in.
        :rtype: int
        """
        return self._page

    @page.setter
    def page(self, page_num: int):
        """
        Sets the page number attribute of the Line entity.

        :param page_num: Page number where the Line entity exists.
        :type page_num: int
        """
        self._page = page_num

    @property
    def page_id(self) -> str:
        """
        :return: Returns the Page ID attribute of the page which the entity belongs to.
        :rtype: str
        """
        return self._page_id

    @page_id.setter
    def page_id(self, page_id: str):
        """
        Sets the Page ID of the :class:`Line` entity.

        :param page_id: Page ID of the page the entity belongs to.
        :type page_id: str
        """
        self._page_id = page_id

    def get_words_by_type(self, text_type: TextTypes = TextTypes.PRINTED) -> List[Word]:
        """
        :param text_type: TextTypes.PRINTED or TextTypes.HANDWRITING
        :type text_type: TextTypes
        :return: Returns EntityList of Word entities that match the input text type.
        :rtype: EntityList[Word]
        """
        if not isinstance(text_type, TextTypes):
            raise InputError(
                "text_type parameter should be of TextTypes type. Find input choices from textractor.data.constants"
            )

        if not self.words:
            return []
        return EntityList([word for word in self.words if word.text_type == text_type])

    def __repr__(self):
        """
        :return: String representation of the Line entity.
        :rtype: str
        """
        return " ".join([word.text for word in self.words])
