from abc import ABC, abstractmethod
from typing import List

from ttsvowelviz.utils import Segment


class ForcedAligner(ABC):
    """Aligns a speech recording with its text transcript."""

    @abstractmethod
    def align(self, text_file_path: str, audio_file_path: str, textgrid_file_path: str) -> None:
        """
        Aligns a speech recording with its text transcript and saves the TextGrid in the same directory as the speech file.
.
        :param text_file_path: Path to the text file.
        :param audio_file_path: Path the speech recording.
        :param textgrid_file_path: Path to the textgrid file.
        """
        raise NotImplementedError("The align method must be implemented by subclasses.")

    @staticmethod
    def read_textgrid(textgrid_file_path: str) -> List[Segment]:
        raise NotImplementedError("The read_textgrid method must be implemented by subclasses.")
