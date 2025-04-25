from typing import List

from ._language import WebMAUSBasicLanguage
from ._logger import _logger as logger
from ._segment import Segment

__all__: List[str] = ["logger", "Segment", "WebMAUSBasicLanguage"]
