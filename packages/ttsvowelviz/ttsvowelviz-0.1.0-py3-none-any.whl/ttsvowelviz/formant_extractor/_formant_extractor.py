from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Union

from pandas import DataFrame
from ttsvowelviz.utils import Segment


class FormantExtractor(ABC):
    """Base class for formant extraction. Subclasses must implement the extraction method."""

    @abstractmethod
    def _extract_formants(self, audio_file_path: str, time: float) -> Tuple[float, float]:
        """
        Extract formants from a given audio file at a given time.

        :param audio_file_path: Path to the audio file.
        :param time: Time in seconds to extract the formants.

        :returns: Extracted F1 and F2 values.
        """
        raise NotImplementedError("The extract_formants method must be implemented by subclasses.")

    def get_static_formants(self, step: str, vowels: List[str], time_points: List[Union[int, float]],
                            segments: List[Segment], audio_file_path: str) -> DataFrame:
        """
        Extracts F1 and F2 formant values at the given time points within each segment to calculate average formant values.

        :param step: Training step.
        :param vowels: A list of vowels.
        :param time_points: A list of time points.
        :param segments: A list of `Segment` objects extracted from the TextGrid file.
        :param audio_file_path: Path to the audio file.

        :returns: A `DataFrame` with average F1 and F2 values per vowel occurrence.
        """
        data: Dict[str, List[Union[str, float]]] = {"vowel": [], f"{step}_f1": [], f"{step}_f2": []}

        for segment in segments:
            if segment.text in vowels:
                data.get("vowel").append(segment.text)
                f1_values, f2_values = [], []  # type:List[float]   # Lists for F1 and F2 values of the segment.

                # Extract formants at each time point within the segment
                for tp in time_points:
                    time_point: float = segment.start_time + ((tp / 100) * (segment.end_time - segment.start_time))
                    f1, f2 = self._extract_formants(audio_file_path=audio_file_path, time=time_point)  # type:float
                    f1_values.append(f1)
                    f2_values.append(f2)

                # Average the extracted formants
                data.get(f"{step}_f1").append((sum(f1_values) / len(f1_values)) if f1_values else None)
                data.get(f"{step}_f2").append((sum(f2_values) / len(f2_values)) if f2_values else None)

        return DataFrame(data=data)

    def get_dynamic_formants(self, step: str, vowels: List[str], time_points: List[Union[int, float]],
                             segments: List[Segment], audio_file_path: str) -> DataFrame:
        """
        Extracts F1 and F2 formant values at the given time points within each segment.

        :param step: Training step.
        :param vowels: A list of vowels.
        :param time_points: A list of time points.
        :param segments: A list of `Segment` objects extracted from the TextGrid file.
        :param audio_file_path: Path to the audio file.

        :returns: A `DataFrame` with F1 and F2 values at each time point per vowel occurrence.
        """
        # Initialize column headers
        data: Dict[str, List[Union[str, float]]] = {
            "vowel": [], **{f"{step}_{round(number=tp, ndigits=2)}%_f1": [] for tp in time_points},
            **{f"{step}_{round(number=tp, ndigits=2)}%_f2": [] for tp in time_points}}

        for segment in segments:
            if segment.text in vowels:
                data.get("vowel").append(segment.text)

                # Extract formants at each time point within the segment
                for tp in time_points:
                    time_point: float = segment.start_time + ((tp / 100) * (segment.end_time - segment.start_time))
                    f1, f2 = self._extract_formants(audio_file_path=audio_file_path, time=time_point)  # type:float
                    data.get(f"{step}_{round(tp, 2)}%_f1").append(f1)
                    data.get(f"{step}_{round(tp, 2)}%_f2").append(f2)

        return DataFrame(data=data)
