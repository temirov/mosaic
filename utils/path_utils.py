from pathlib import Path
from typing import Iterator

import constants
from services.mime_detection_service import MimeDetectionService


class PathUtils:
    @classmethod
    def glob_path_walker(cls, folder: str, glob_pattern: str, recursive: bool = None,
                         excluded_paths: list[Path] = None) -> Iterator[Path]:
        if recursive is None:
            recursive = False
        if excluded_paths is None:
            excluded_paths = []

        def walker(directory, glob):
            if recursive:
                return Path(directory).rglob(glob)
            else:
                return Path(directory).glob(glob)

        for path in walker(folder, glob_pattern):
            if not cls.__is_excluded__(path, excluded_paths):
                yield path

    @classmethod
    def raise_when_no_folder(cls, folder: str) -> None:
        if not cls.dir_exists(folder):
            raise RuntimeError(f"Folder {folder} does not exist")

    @classmethod
    def raise_when_no_file(cls, file_path: str) -> None:
        if not cls.file_exists(file_path):
            raise RuntimeError(f"File {file_path} does not exist")

    @classmethod
    def is_hidden(cls, path: Path) -> bool:
        return any(part.startswith('.') for part in path.parts)

    @classmethod
    def is_in_folder(cls, path: Path, folder: str) -> bool:
        return any(part == folder for part in path.parts)

    @classmethod
    def is_empty_file(cls, path: Path) -> bool:
        return path.is_file() and path.stat().st_size == 0

    @classmethod
    def is_empty_dir(cls, path: Path) -> bool:
        return path.is_dir() and not any(path.iterdir())

    @classmethod
    def is_mac_system_file(cls, path: Path) -> bool:
        return path.is_file() and path.name == constants.MAC_DS_STORE

    @classmethod
    def dir_exists(cls, value: str) -> bool:
        path = cls.as_path(value)
        return path.exists() and path.is_dir()

    @classmethod
    def file_exists(cls, value: str) -> bool:
        path = cls.as_path(value)
        return path.exists() and path.is_file()

    @classmethod
    def is_plaintext_file(cls, path: Path) -> bool:
        file_type = cls.__get_file_type__(path)
        return path.is_file() and file_type == constants.PLAIN_TEXT_MIME_SUBTYPE

    @classmethod
    def is_pdf_file(cls, path: Path) -> bool:
        file_type = cls.__get_file_type__(path)
        return file_type == constants.PDF_MIME_SUBTYPE

    @classmethod
    def is_image_file(cls, path: Path) -> bool:
        file_type = cls.__get_file_type__(path)
        return file_type.split("/")[0] == constants.IMAGE_MIME_TYPE

    @classmethod
    def is_json_file(cls, path: Path) -> bool:
        file_type = cls.__get_file_type__(path)
        return file_type == constants.JSON_MIME_SUBTYPE

    @classmethod
    def is_application_file(cls, path: Path) -> bool:
        file_type = cls.__get_file_type__(path)
        return file_type.split("/")[0] == constants.APPLICATION_MIME_TYPE

    @classmethod
    def is_md_candidate(cls, path: Path) -> bool:
        return path.is_file() and path.suffix == constants.EMPTY_STRING and cls.is_plaintext_file(path)

    @classmethod
    def is_markup_file(cls, path: Path) -> bool:
        return path.is_file() and path.name.endswith(constants.MARKDOWN_EXTENSION)

    @classmethod
    def as_path(cls, value: str) -> Path:
        return Path(value)

    @classmethod
    def __get_file_type__(cls, path: Path) -> str:
        mime_detection_service = MimeDetectionService(path)
        return mime_detection_service()

    @classmethod
    def __is_excluded__(cls, path: Path, excluded_paths: list[Path]) -> bool:
        return any(path.is_relative_to(excluded) for excluded in excluded_paths)
