import subprocess
from pathlib import Path

import magic


class MimeDetectionService:
    def __init__(self, path: Path):
        self.path = path
        self.mime_detector = magic.Magic(mime=True, uncompress=True)

    def __call__(self, *args, **kwargs) -> str:
        try:
            result = subprocess.check_output(['file', '-b', '--mime', self.path.absolute().as_posix()],
                                             universal_newlines=True)
            return result.split(";")[0]
        except subprocess.CalledProcessError:
            return self.mime_detector.from_file(self.path.as_posix())
