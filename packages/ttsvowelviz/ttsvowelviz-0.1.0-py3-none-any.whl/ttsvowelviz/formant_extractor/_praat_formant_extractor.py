from os.path import isfile
from typing import Optional, Tuple

from parselmouth import Formant, Sound
from ttsvowelviz.utils.constants import LOG_PREFIX

from ._formant_extractor import FormantExtractor


class PraatFormantExtractor(FormantExtractor):
    """Formant extractor implementation using Praat via Parselmouth."""

    def __init__(self, unit: str = "BARK") -> None:
        super().__init__()
        self._unit: str = unit  # Unit of formant frequency. Defaults to Bark.
        self._audio_file_path: Optional[str] = None
        self._formants: Optional[Formant] = None

    def _extract_formants(self, audio_file_path: str, time: float) -> Tuple[float, float]:
        """
        Extract formants from a given audio file at a given time.

        :param audio_file_path: Path to the `.wav` file.
        :param time: Time in seconds to extract the formants.

        :returns: Extracted F1 and F2 values.
        :raises FileNotFoundError: If the audio file does not exist.
        """
        # Check if the audio file exists
        if not isfile(path=audio_file_path):
            raise FileNotFoundError(f"{LOG_PREFIX} Audio file not found: {audio_file_path}")

        # Only re-extract formants if the audio file path has changed
        if audio_file_path != self._audio_file_path:
            self._audio_file_path: str = audio_file_path
            self._formants: Formant = Sound(audio_file_path).to_formant_burg(time_step=None)

        # Extract the first and second formants (F1 and F2) at the given time
        f1: float = self._formants.get_value_at_time(formant_number=1, time=time, unit=self._unit)
        f2: float = self._formants.get_value_at_time(formant_number=2, time=time, unit=self._unit)
        return f1, f2
