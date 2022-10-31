import difflib
import re
from typing import Iterator, Optional

import constants


class StringUtils:
    @classmethod
    def content_diff(cls, content1, content2) -> str:
        content_list1 = cls.__cr_split__(content1)
        content_list2 = cls.__cr_split__(content2)
        mismatches = difflib.Differ().compare(content_list1, content_list2)
        return cls.__cr_join__(mismatches)

    @classmethod
    def remove_substring(cls, string: str, substring: str) -> str:
        return string.replace(substring, constants.EMPTY_STRING)

    @classmethod
    def has_glob_suffix(cls, string: str, suffix: str) -> bool:
        suffix_with_no_glob = cls.__suffix_with_no_glob(suffix)
        return string is not None and suffix is not None and suffix_with_no_glob in string

    @classmethod
    def expand_and_remove_suffix(cls, file_path: str, suffix: str) -> str:
        suffix_with_no_glob = cls.__suffix_with_no_glob(suffix)
        expanded_regex_with_groups = f"(.+?)({suffix_with_no_glob}.*)(\..*)"
        return re.sub(expanded_regex_with_groups, r'\1\3', file_path)

    @classmethod
    def has_suffix(cls, string: str, suffix: str) -> bool:
        return string.endswith(suffix)

    @classmethod
    def remove_suffix(cls, string: str, suffix: str) -> str:
        return string.removesuffix(suffix)

    @classmethod
    def as_before_glob(cls, string) -> str:
        return f"*{string}"

    @classmethod
    def __suffix_with_no_glob(cls, suffix: str):
        return cls.remove_substring(suffix, "*")

    @classmethod
    def __cr_split__(cls, content: str) -> list[str]:
        return content.split(constants.UNIX_CR)

    @classmethod
    def __cr_join__(cls, content: Iterator[str]) -> str:
        return constants.UNIX_CR.join(content)

    @classmethod
    def trim(cls, content: str, top: Optional[int] = None, bottom: Optional[int] = None) -> Iterator[str]:
        """
        Removes top and bottom lines in the text
        :param content: multi-lined text, separated by CR
        :param top: the number of lines to remove from the top
        :param bottom: the number of lines to remove from the bottom
        :return:
        """
        if top is None:
            top = 1
        if bottom is None:
            bottom = -1
        content_list = cls.__cr_split__(content)
        trimmed_content = content_list[top:bottom]
        return cls.__cr_join__(trimmed_content)
