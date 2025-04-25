from abc import ABC, abstractmethod


class Synthesizer(ABC):
    """
    Base class that all synthesizers should inherent for any TTS model.
    """

    @abstractmethod
    def synthesize(self, step: int, text: str) -> str:
        """
        Synthesize speech from text.

        :param step: The number of training steps that the intermediate model used for synthesis should be trained on.
        :param text: The input text to synthesize.

        :return: Path to the synthesized audio file.
        """
        raise NotImplementedError("The synthesize method must be implemented by subclasses.")
