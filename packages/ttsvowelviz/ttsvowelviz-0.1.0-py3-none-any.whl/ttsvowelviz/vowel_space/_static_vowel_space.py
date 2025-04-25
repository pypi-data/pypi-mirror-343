from typing import Dict, List, Optional, Union

from pandas import DataFrame, read_csv
from plotly.graph_objects import Figure, Frame, Scatter
from ttsvowelviz.utils.constants import STATIC_FORMANTS_FILE_PATH, STATIC_VOWEL_SPACE_FILE_PATH

from ._vowel_space import VowelSpace


class StaticVowelSpace(VowelSpace):
    def __init__(self, intermediate_steps: List[int], point_vowels: List[str],
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

    def plot(self, step: int) -> None:
        df: DataFrame = read_csv(filepath_or_buffer=STATIC_FORMANTS_FILE_PATH)  # Formants dataframe

        figure: Figure = Figure()  # Vowel space figure
        frames: List[Frame] = []  # List of frames for each step
        # Initialize plot
        for _ in range(len(df) + 2):  # (+2) for the ground truth and synthesized vowel space shapes
            figure.add_trace(trace=Scatter())

        # Add ground truth values as the first frame
        truth_frame_traces: List[Scatter] = []
        for index, row in df.iterrows():
            color: str = self._get_color_by_index(index=int(index.__str__()))
            truth_frame_traces.append(
                Scatter(x=[row["truth_f2"]], y=[row["truth_f1"]], mode="markers+text",
                        marker=dict(size=10, color=color, symbol=["x"]),
                        text=self._vowel_labels.get(row["vowel"], row["vowel"]), textposition="top center",
                        textfont=dict(color=color),
                        name=self._vowel_labels.get(row["vowel"], row["vowel"]), showlegend=True, visible=True))

        # Plot ground truth vowel space shape by connecting point vowels
        truth_frame_traces.append(self._plot_ground_truth_vowel_space_shape(df=df))
        # showlegend=False, visible=False: Because the synthesized vowel space is not present here
        truth_frame_traces.append(Scatter(showlegend=False, visible=False))

        frames.append(Frame(data=truth_frame_traces, name="Ground Truth"))

        steps: List[int] = self._get_steps(df=df, max_step=step)
        # Add frames for each training step
        for s in steps:
            # Get all step columns that are lower than the current step and end with "f1" or "f2"
            f1_cols: List[str] = [col for col in df.columns if (not col.startswith("truth"))
                                  and col.endswith("f1") and (int(col.split(sep="_")[0]) <= s)]
            f2_cols: List[str] = [col for col in df.columns if (not col.startswith("truth"))
                                  and col.endswith("f2") and (int(col.split(sep="_")[0]) <= s)]

            # Sort columns based on the step to maintain a consistent order
            f1_cols: List[str] = sorted(f1_cols, key=lambda x: int(x.split(sep="_")[0]))
            f2_cols: List[str] = sorted(f2_cols, key=lambda x: int(x.split(sep="_")[0]))

            step_frame_traces: List[Scatter] = []

            for index, row in df.iterrows():
                # Extract f1 and f2 values
                f1_values, f2_values = [row[col] for col in f1_cols], [row[col] for col in f2_cols]  # type:List[float]
                color: str = self._get_color_by_index(index=int(index.__str__()))

                # Create a trace by connecting points with lines. "None" is to disconnect the ground truth point from the synthesized.
                step_frame_traces.append(
                    Scatter(x=[row["truth_f2"], None] + f2_values, y=[row["truth_f1"], None] + f1_values,
                            mode="lines+markers+text", line=dict(color=color),
                            marker=dict(size=6, color=color, symbol=["x", "circle"]),
                            text=[self._vowel_labels.get(row["vowel"], row["vowel"]), None]
                                 + [i.__str__() for i in range(len(f1_values))],
                            textposition="top center", textfont=dict(color=color),
                            name=self._vowel_labels.get(row["vowel"], row["vowel"]), showlegend=True, visible=True))

            # Plot ground truth vowel space shape by connecting point vowels
            step_frame_traces.append(self._plot_ground_truth_vowel_space_shape(df=df))
            # Plot synthesized vowel space shape by connecting point vowels
            step_frame_traces.append(self._plot_synthesized_vowel_space_shape(df=df, step=s))

            frames.append(Frame(data=step_frame_traces, name=f"{s}"))

        figure.frames = frames  # Add frames to the figure

        # Set up the figure layout
        figure.update_layout(
            title="Static Vowel Space", xaxis_title=self._x_axis_title, yaxis_title=self._y_axis_title,
            xaxis=dict(range=self._x_axis_range, autorange=False),
            yaxis=dict(range=self._y_axis_range, autorange=False),
            template=self._figure_template, height=self._figure_height, width=self._figure_width,
            updatemenus=self._figure_layout_update_menus,
            sliders=[dict(steps=[
                dict(args=[[f"{s}"], dict(frame=dict(duration=0, redraw=True), mode="immediate")], label=f"{s}",
                     method="animate") for s in ["Ground Truth"] + steps], currentvalue=dict(prefix="Step: "))])

        figure.write_html(file=STATIC_VOWEL_SPACE_FILE_PATH)
