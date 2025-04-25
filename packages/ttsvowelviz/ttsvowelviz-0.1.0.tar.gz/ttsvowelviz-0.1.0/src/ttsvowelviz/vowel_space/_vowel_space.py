from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Set, Union

from pandas import DataFrame
from plotly.graph_objs import Scatter


class VowelSpace(ABC):
    def __init__(self, intermediate_steps: List[int], point_vowels: List[str],
                 vowel_labels: Optional[Dict[str, str]] = None,
                 x_axis_title: Optional[str] = None, y_axis_title: Optional[str] = None,
                 x_axis_range: Optional[List[Union[int, float]]] = None,
                 y_axis_range: Optional[List[Union[int, float]]] = None,
                 figure_template: Optional[str] = None,
                 figure_height: Optional[int] = None, figure_width: Optional[int] = None) -> None:
        self._intermediate_steps: List[int] = intermediate_steps
        self._point_vowels: List[str] = point_vowels
        self._vowel_labels: Dict[str, str] = vowel_labels if vowel_labels else {}
        self._x_axis_title: str = x_axis_title if x_axis_title else "F2"
        self._y_axis_title: str = y_axis_title if y_axis_title else "F1"
        # Reverse axes by setting range from high to low
        self._x_axis_range: List[Union[int, float]] = sorted(x_axis_range, reverse=True) if x_axis_range else [20, 0]
        self._y_axis_range: List[Union[int, float]] = sorted(y_axis_range, reverse=True) if y_axis_range else [10, 0]
        self._figure_template: str = figure_template if figure_template else "plotly_white"  # ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]
        self._figure_height: int = figure_height if figure_height else 700
        self._figure_width: int = figure_width if figure_width else 800
        self._figure_layout_update_menus: List[dict] = [
            dict(type="buttons", showactive=False,
                 buttons=[dict(label="Play", method="animate", args=[None,
                                                                     dict(frame=dict(duration=500, redraw=True),
                                                                          fromcurrent=True)]),
                          dict(label="Pause", method="animate", args=[[None],
                                                                      dict(frame=dict(duration=0, redraw=True),
                                                                           mode="immediate", fromcurrent=True)])])]

    @staticmethod
    def _get_color_by_index(index: int) -> str:
        """
        Hue (0–360): The color itself (red, green, blue, etc.).
        Saturation (0%–100%): How vivid the color is (0% = gray, 100% = full color).
        Lightness (0%–100%): How light or dark the color is (0% = black, 100% = white, 50% = "normal" color).
        """
        # H: Multiplies index by 50 to create spacing between hues. Uses % 360 to wrap around after reaching 360 (since hue is circular). So for increasing x values, you get a repeating, evenly spaced set of hues.
        # S (70%): Fixed, meaning the color is pretty vivid.
        # L (50%): Fixed, meaning you're in the middle range — not too dark, not too bright.
        return f"hsl({index * 50 % 360}, 70%, 50%)"

    def _plot_ground_truth_vowel_space_shape(self, df: DataFrame) -> Scatter:
        # Plot ground truth vowel space shape by connecting point vowels
        point_vowels_df: DataFrame = df.set_index(keys="vowel").loc[self._point_vowels][["truth_f1", "truth_f2"]]
        return Scatter(x=point_vowels_df["truth_f2"].tolist() + [point_vowels_df["truth_f2"].iloc[0]],
                       y=point_vowels_df["truth_f1"].tolist() + [point_vowels_df["truth_f1"].iloc[0]],
                       mode="lines", line=dict(width=1, dash="dot"),
                       name="Ground Truth Vowel Space Shape", showlegend=True, visible=True)

    def _plot_synthesized_vowel_space_shape(self, df: DataFrame, step: int) -> Scatter:
        # Plot synthesized vowel space shape by connecting point vowels
        point_vowels_df: DataFrame = df.set_index(keys="vowel").loc[self._point_vowels][[f"{step}_f1", f"{step}_f2"]]
        return Scatter(x=point_vowels_df[f"{step}_f2"].tolist() + [point_vowels_df[f"{step}_f2"].iloc[0]],
                       y=point_vowels_df[f"{step}_f1"].tolist() + [point_vowels_df[f"{step}_f1"].iloc[0]],
                       mode="lines", line=dict(width=1, dash="dot"),
                       name="Synthesized Vowel Space Shape", showlegend=True, visible=True)

    def _get_steps(self, df: DataFrame, max_step: int) -> List[int]:
        """
        Extracts steps from the `DataFrame` column names that are less than or equal to max_step, and returns the common steps between those extracted and the given intermediate_steps.

        :param df: Formants `DataFrame`
        :param max_step: Maximum step to consider.
        :returns: List of steps sorted in ascending order.
        """
        # Extract steps lower than the given steps
        df_steps: Set[int] = {int(col.split(sep="_")[0]) for col in df.columns
                              if col.split(sep="_")[0].isdigit() and int(col.split(sep="_")[0]) <= max_step}
        return sorted(df_steps.intersection(self._intermediate_steps))

    @abstractmethod
    def plot(self, step: int) -> None:
        raise NotImplementedError("The plot method must be implemented by subclasses.")
