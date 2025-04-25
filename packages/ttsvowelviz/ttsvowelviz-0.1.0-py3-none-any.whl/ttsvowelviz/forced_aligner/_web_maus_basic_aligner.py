from re import search
from subprocess import CompletedProcess, run
from typing import List
from urllib.request import urlretrieve

from tgt.core import Interval
from tgt.io import read_textgrid
from ttsvowelviz.utils import Segment, WebMAUSBasicLanguage
from ttsvowelviz.utils.constants import LOG_PREFIX

from ._forced_aligner import ForcedAligner


class WebMAUSBasicAligner(ForcedAligner):
    """Computes a phonetic segmentation and labeling for several languages based on the speech signal and a phonological transcript encoded in SAM-PA."""

    def __init__(self, language: str) -> None:
        try:
            super().__init__()
            self.__language: str = WebMAUSBasicLanguage(language).value
        except ValueError:
            raise ValueError(f"{LOG_PREFIX} Language is not a valid WebMAUSBasicLanguage.")

    def align(self, text_file_path: str, audio_file_path: str, textgrid_file_path: str) -> None:
        """
        Aligns a speech recording with its text transcript and saves the TextGrid in the same directory as the speech file.
.
        :param text_file_path: Path to the text file.
        :param audio_file_path: Path the speech recording.
        :param textgrid_file_path: Path to the textgrid file.
        """
        curl_cmd: List[str] = [
            "curl",
            "-X", "POST",
            "-F", f"SIGNAL=@{audio_file_path};type=audio/wav",
            "-F", f"TEXT=@{text_file_path};type=text/plain",
            "-F", f"LANGUAGE={self.__language}",
            "-F", "OUTFORMAT=TextGrid",
            "https://clarin.phonetik.uni-muenchen.de/BASWebServices/services/runMAUSBasic"
        ]

        response: CompletedProcess = run(args=curl_cmd, capture_output=True, text=True)
        textgrid_url: str = search(pattern=r"<downloadLink>(.*?)</downloadLink>", string=response.stdout).group(1)
        urlretrieve(url=textgrid_url, filename=textgrid_file_path)

    @staticmethod
    def read_textgrid(textgrid_file_path: str) -> List[Segment]:
        intervals: List[Interval] = read_textgrid(filename=textgrid_file_path).get_tier_by_name(name="MAU").intervals
        segments: List[Segment] = []
        for i in intervals:
            segments.append(Segment(text=i.text, start_time=i.start_time, end_time=i.end_time))
        return segments
