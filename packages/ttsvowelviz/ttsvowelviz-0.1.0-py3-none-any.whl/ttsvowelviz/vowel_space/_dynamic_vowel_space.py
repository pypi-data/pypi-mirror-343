from typing import Dict, List, Optional, Tuple, Union

from numpy import linspace
from pandas import DataFrame, read_csv
from plotly.graph_objects import Figure, Frame, Scatter
from ttsvowelviz.utils.constants import DYNAMIC_FORMANTS_FILE_PATH, DYNAMIC_VOWEL_SPACE_FILE_PATH, \
    STATIC_FORMANTS_FILE_PATH

from ._vowel_space import VowelSpace


class DynamicVowelSpace(VowelSpace):
    def __init__(self, intermediate_steps: List[int], time_points: List[Union[int, float]], point_vowels: List[str],
                 vowel_labels: Optional[Dict[str, str]] = None,
                 x_axis_title: Optional[str] = None, y_axis_title: Optional[str] = None,
                 x_axis_range: Optional[List[Union[int, float]]] = None,
                 y_axis_range: Optional[List[Union[int, float]]] = None,
                 figure_template: Optional[str] = None,
                 figure_height: Optional[int] = None, figure_width: Optional[int] = None) -> None:
        super().__init__(intermediate_steps=intermediate_steps, point_vowels=point_vowels, vowel_labels=vowel_labels,
                         x_axis_title=x_axis_title, y_axis_title=y_axis_title,
                         x_axis_range=x_axis_range, y_axis_range=y_axis_range,
                         figure_template=figure_template, figure_height=figure_height, figure_width=figure_width)
        self._time_points: List[Union[int, float]] = [round(number=n, ndigits=2) for n in time_points]

    def _get_column_names(self, step: str, df: DataFrame) -> Tuple[List[str], List[str]]:
        f1_cols, f2_cols = [], []  # type: List[str]
        columns: List[str] = [col for col in df.columns if col != "vowel"]
        for col in columns:
            splits: List[str] = col.split(sep="_")
            if (splits[0] == step) and (float(splits[1].replace("%", "")) in self._time_points):
                f1_cols.append(col) if (splits[2] == "f1") else f2_cols.append(col)
        return f1_cols, f2_cols

    def plot(self, step: int) -> None:
        static_df: DataFrame = read_csv(filepath_or_buffer=STATIC_FORMANTS_FILE_PATH)  # Static vowel formants
        dynamic_df: DataFrame = read_csv(filepath_or_buffer=DYNAMIC_FORMANTS_FILE_PATH)  # Dynamic vowel formants

        figure: Figure = Figure()  # Vowel space figure
        frames: List[Frame] = []  # List of frames for each step
        # Initialize plot
        for _ in range(len(static_df) + len(dynamic_df) + 1):  # (+1) for ground truth or synthesized vowel space shape
            figure.add_trace(trace=Scatter())

        # Add ground truth values as the first frame
        truth_frame_traces: List[Scatter] = []
        for index, row in static_df.iterrows():
            color: str = self._get_color_by_index(index=int(index.__str__()))
            truth_frame_traces.append(
                Scatter(x=[row["truth_f2"]], y=[row["truth_f1"]], mode="markers+text",
                        marker=dict(size=10, color=color, symbol=["x"]),
                        text=self._vowel_labels.get(row["vowel"], row["vowel"]), textposition="top center",
                        textfont=dict(color=color),
                        name=self._vowel_labels.get(row["vowel"], row["vowel"]), showlegend=False, visible=True))

        # Plot ground truth vowel space shape by connecting point vowels
        truth_frame_traces.append(self._plot_ground_truth_vowel_space_shape(df=static_df))

        truth_f1_cols, truth_f2_cols = self._get_column_names(step="truth", df=dynamic_df)  # type: List[str]
        for index, row in dynamic_df.iterrows():
            color: str = self._get_color_by_index(index=len(static_df) + int(index.__str__()))
            truth_frame_traces.append(
                Scatter(x=[row[col] for col in truth_f2_cols], y=[row[col] for col in truth_f1_cols],
                        mode="lines+markers", line=dict(shape="spline", smoothing=1.3, color=color, width=1.5),
                        marker=dict(size=linspace(start=4, stop=8, num=len(truth_f1_cols)), symbol="x", color=color),
                        name=self._vowel_labels.get(row["vowel"], row["vowel"]), showlegend=True, visible=True))

        frames.append(Frame(data=truth_frame_traces, name="Ground Truth"))

        steps: List[int] = self._get_steps(df=dynamic_df, max_step=step)
        # Add frames for each training step
        for s in steps:
            step_frame_traces: List[Scatter] = []

            for index, row in static_df.iterrows():
                color: str = self._get_color_by_index(index=int(index.__str__()))
                # Create a trace by connecting points with lines. "None" is to disconnect the ground truth point from the synthesized.
                step_frame_traces.append(
                    Scatter(x=[row[f"{s}_f2"]], y=[row[f"{s}_f1"]], mode="markers+text",
                            marker=dict(size=6, color=color, symbol=["circle"]),
                            text=self._vowel_labels.get(row["vowel"], row["vowel"]), textposition="top center",
                            textfont=dict(color=color),
                            name=self._vowel_labels.get(row["vowel"], row["vowel"]), showlegend=False, visible=True))

            # Plot synthesized vowel space shape by connecting point vowels
            step_frame_traces.append(self._plot_synthesized_vowel_space_shape(df=static_df, step=s))

            step_f1_cols, step_f2_cols = self._get_column_names(step=s.__str__(), df=dynamic_df)  # type: List[str]
            for index, row in dynamic_df.iterrows():
                color: str = self._get_color_by_index(index=len(static_df) + int(index.__str__()))
                step_frame_traces.append(
                    Scatter(x=[row[col] for col in step_f2_cols], y=[row[col] for col in step_f1_cols],
                            mode="lines+markers", line=dict(shape="spline", smoothing=1.3, color=color, width=1.5),
                            marker=dict(size=linspace(start=4, stop=8, num=len(truth_f1_cols)), symbol="circle",
                                        color=color),
                            name=self._vowel_labels.get(row["vowel"], row["vowel"]), showlegend=True, visible=True))

            frames.append(Frame(data=step_frame_traces, name=f"{s}"))

        figure.frames = frames  # Add frames to the figure

        # Set up the figure layout
        figure.update_layout(
            title="Dynamic Vowel Space", xaxis_title=self._x_axis_title, yaxis_title=self._y_axis_title,
            xaxis=dict(range=self._x_axis_range, autorange=False),
            yaxis=dict(range=self._y_axis_range, autorange=False),
            template=self._figure_template, height=self._figure_height, width=self._figure_width,
            updatemenus=self._figure_layout_update_menus,
            sliders=[dict(steps=[
                dict(args=[[f"{s}"], dict(frame=dict(duration=0, redraw=True), mode="immediate")], label=f"{s}",
                     method="animate") for s in ["Ground Truth"] + steps], currentvalue=dict(prefix="Step: "))])

        figure.write_html(file=DYNAMIC_VOWEL_SPACE_FILE_PATH)
