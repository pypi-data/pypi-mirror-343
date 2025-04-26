from abc import ABC, abstractmethod
from typing import List, Optional, Set, Tuple

from maytak.data_structures.attached_file import AttachedFile


class AbstractAttachmentsExtractor(ABC):

    def __init__(self, *, config: Optional[dict] = None, recognized_extensions: Optional[Set[str]] = None, recognized_mimes: Optional[Set[str]] = None) -> None:

        import logging

        self.config = {} if config is None else config
        self.logger = self.config.get("logger", logging.getLogger())
        self._recognized_extensions = {} if recognized_extensions is None else recognized_extensions
        self._recognized_mimes = {} if recognized_mimes is None else recognized_mimes

    def can_extract(self,
                    file_path: Optional[str] = None,
                    extension: Optional[str] = None,
                    mime: Optional[str] = None,
                    parameters: Optional[dict] = None) -> bool:
        from maytak.utils.utils import get_mime_extension
        mime, extension = get_mime_extension(file_path=file_path, mime=mime, extension=extension)
        return extension.lower() in self._recognized_extensions or mime in self._recognized_mimes

    @abstractmethod
    def extract(self, file_path: str, parameters: Optional[dict] = None) -> List[AttachedFile]:
        pass

    @staticmethod
    def with_attachments(parameters: dict) -> bool:

        return str(parameters.get("with_attachments", "false")).lower() == "true"

    def _content2attach_file(self, content: List[Tuple[str, bytes]], tmpdir: str, need_content_analysis: bool, parameters: dict) -> List[AttachedFile]:
        import os
        import uuid
        from maytak.utils.parameter_utils import get_param_attachments_dir
        from maytak.utils.utils import save_data_to_unique_file

        attachments = []

        attachments_dir = get_param_attachments_dir(parameters, tmpdir)

        for original_name, contents in content:
            tmp_file_name = save_data_to_unique_file(directory=attachments_dir, filename=original_name, binary_data=contents)
            tmp_file_path = os.path.join(attachments_dir, tmp_file_name)
            file = AttachedFile(original_name=original_name,
                                tmp_file_path=tmp_file_path,
                                uid=f"attach_{uuid.uuid4()}",
                                need_content_analysis=need_content_analysis)
            attachments.append(file)
        return attachments
