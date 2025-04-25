from os import listdir, makedirs
from os.path import exists, isdir, join, splitext
from shutil import copy, copytree, rmtree
from typing import Dict, List, Optional, Set, Tuple, Union

from pandas import concat, DataFrame, merge, read_csv
from ttsvowelviz.forced_aligner import ForcedAligner
from ttsvowelviz.formant_extractor import FormantExtractor
from ttsvowelviz.utils import logger, Segment
from ttsvowelviz.utils.constants import DATA_DIRECTORY_PATH, DYNAMIC_FORMANTS_FILE_PATH, FILE_NAME_PREFIX, \
    FORMANTS_DIRECTORY_PATH, GROUND_TRUTH_DIRECTORY_NAME, GROUND_TRUTH_DIRECTORY_PATH, SPEECH_DIRECTORY_PATH, \
    STATIC_FORMANTS_FILE_PATH, TEXT_DIRECTORY_PATH, VOWEL_SPACE_DIRECTORY_PATH
from ttsvowelviz.vowel_space import DynamicVowelSpace, StaticVowelSpace

from ._synthesizer import Synthesizer


class TTSVowelViz(object):
    def __init__(self, static_vowels: List[str], static_time_points: List[Union[int, float]], point_vowels: List[str],
                 dynamic_vowels: List[str], dynamic_time_points: List[Union[int, float]], intermediate_steps: List[int],
                 synthesizer: Synthesizer, forced_aligner: ForcedAligner, formant_extractor: FormantExtractor,
                 text_list: List[str], ground_truth_src_dir_path: str, vowel_space_dst_dir_path: str,
                 process_ground_truth: bool = False, vowel_labels: Optional[Dict[str, str]] = None,
                 x_axis_title: Optional[str] = None, y_axis_title: Optional[str] = None,
                 x_axis_range: Optional[List[Union[int, float]]] = None,
                 y_axis_range: Optional[List[Union[int, float]]] = None,
                 figure_template: Optional[str] = None,
                 figure_height: Optional[int] = None, figure_width: Optional[int] = None) -> None:
        self._static_vowels: List[str] = static_vowels
        self._static_time_points: List[Union[int, float]] = sorted(static_time_points)
        self._point_vowels: List[str] = point_vowels
        self._dynamic_vowels: List[str] = dynamic_vowels
        self._dynamic_time_points: List[Union[int, float]] = sorted(dynamic_time_points)
        self._intermediate_steps: List[int] = sorted(intermediate_steps)
        self._synthesizer: Synthesizer = synthesizer
        self._forced_aligner: ForcedAligner = forced_aligner
        self._formant_extractor: FormantExtractor = formant_extractor
        self._vowel_space_dst_dir_path: str = vowel_space_dst_dir_path
        self._vowel_labels: Optional[Dict[str, str]] = vowel_labels
        self._x_axis_title: Optional[str] = x_axis_title
        self._y_axis_title: Optional[str] = y_axis_title
        self._x_axis_range: Optional[List[Union[int, float]]] = x_axis_range
        self._y_axis_range: Optional[List[Union[int, float]]] = y_axis_range
        self._figure_template: Optional[str] = figure_template
        self._figure_height: Optional[int] = figure_height
        self._figure_width: Optional[int] = figure_width
        self._preprocess(text_list=text_list, process_ground_truth=process_ground_truth,
                         ground_truth_src_dir_path=ground_truth_src_dir_path)

    def _preprocess(self, text_list: List[str], process_ground_truth: bool, ground_truth_src_dir_path: str) -> None:
        makedirs(name=DATA_DIRECTORY_PATH, exist_ok=True)  # Create the data directory if it doesn't exist
        makedirs(name=SPEECH_DIRECTORY_PATH, exist_ok=True)  # Create the speech directory if it doesn't exist
        makedirs(name=FORMANTS_DIRECTORY_PATH, exist_ok=True)  # Create the formants directory if it doesn't exist
        makedirs(name=VOWEL_SPACE_DIRECTORY_PATH,
                 exist_ok=True)  # Create the vowel_spaces directory if it doesn't exist

        # Ensure the text list is not empty
        if not text_list:
            raise ValueError(f"text_list cannot be empty.")

        # Remove the text directory if it already exists
        if exists(path=TEXT_DIRECTORY_PATH):
            rmtree(path=TEXT_DIRECTORY_PATH)
        makedirs(name=TEXT_DIRECTORY_PATH)  # Create a new text directory

        # Loop through the list and write each text to a separate txt file
        for i, content in enumerate(iterable=text_list, start=1):
            with open(file=join(TEXT_DIRECTORY_PATH, f"{FILE_NAME_PREFIX}{i}.txt"), mode="w") as file:
                file.write(content.strip())

        only_compute_formants: bool = False if (process_ground_truth or (not exists(path=GROUND_TRUTH_DIRECTORY_PATH))) \
            else True
        self.process_ground_truth(ground_truth_src_dir_path=ground_truth_src_dir_path,
                                  only_compute_formants=only_compute_formants)

    def _synthesize_at_step(self, step: int, file_names: Set[str]) -> None:
        logger.info(msg=f"Speech synthesis is in progress at step: {step}")
        for f in file_names:
            with open(file=join(TEXT_DIRECTORY_PATH, f"{f}.txt"), mode="r") as file:
                synthesized_speech_file_path: str = self._synthesizer.synthesize(step=step, text=file.read().strip())
                if not exists(path=synthesized_speech_file_path):
                    raise FileNotFoundError(f"Synthesized speech file doesn't exist at {synthesized_speech_file_path}")
                copy(src=synthesized_speech_file_path,
                     dst=join(SPEECH_DIRECTORY_PATH, step.__str__(), f"{f}.wav"))
                logger.info(msg=f"\t└── {f}")
        logger.info(msg=f"Speech synthesis completed at step: {step}")

    def _align_speech_at_step(self, step: str, file_names: Set[str]) -> None:
        logger.info(msg=f"Segmentation is in progress at step: {step}. This may take a while...")
        for f in file_names:
            text_file_path: str = join(TEXT_DIRECTORY_PATH, f"{f}.txt") \
                if not (step == GROUND_TRUTH_DIRECTORY_NAME) else join(SPEECH_DIRECTORY_PATH, step, f"{f}.txt")
            audio_file_path: str = join(SPEECH_DIRECTORY_PATH, step, f"{f}.wav")
            textgrid_file_path: str = join(SPEECH_DIRECTORY_PATH, step, f"{f}.TextGrid")
            self._forced_aligner.align(text_file_path=text_file_path, audio_file_path=audio_file_path,
                                       textgrid_file_path=textgrid_file_path)
            logger.info(msg=f"\t└── {f}")
        logger.info(msg=f"Segmentation completed at step: {step}")

    @staticmethod
    def _update_formants_file(df: DataFrame, file_path: str) -> None:
        def sort_column_names(name: str) -> Tuple[int, Union[str, int], float, Union[str, int]]:
            # Ensure "vowel" is always first
            if name == "vowel":
                return 0, "", 0.0, ""

            splits: List[str] = name.split(sep="_")
            if len(splits) == 2:
                group_name, percentage, f_type = splits[0], -1.0, splits[1]
            else:
                group_name, percentage, f_type = splits[0], float(splits[1].replace("%", "")), splits[2]

            # Assign group: "vowel" = 0, "truth" = 1, others = 2
            if group_name == GROUND_TRUTH_DIRECTORY_NAME:
                group_order: int = 1
                name_sort: int = -1  # Force "truth" to be sorted before numeric groups even though it's not a number
            else:
                group_order: int = 2
                name_sort: int = int(group_name)  # Convert to int for correct numeric sorting (e.g., 1000 before 10000)

            f_order: int = 0 if f_type == "f1" else 1  # Ensure f1 comes before f2

            # Return a tuple used for sorting: (group_order, name_sort, percent_value, f_order)
            return group_order, name_sort, percentage, f_order

        if not df.empty:
            df: DataFrame = df.groupby(by="vowel").mean().reset_index()  # Group by vowel and calculate the mean
            if exists(path=file_path):
                existing_df: DataFrame = read_csv(filepath_or_buffer=file_path)
                merged_df: DataFrame = merge(left=existing_df, right=df, how="outer", on="vowel",
                                             suffixes=("", "_replace"))

                # Replace columns in formant_dataframe with those from vowel_df wherever there’s overlap
                for col in df.columns:
                    if (col != "vowel") and (col in existing_df.columns):
                        # Replace values in original column with values from the "_replace" column where not null
                        merged_df[col] = merged_df[f"{col}_replace"].combine_first(other=merged_df[col])
                        # Drop the "_replace" column after replacement
                        merged_df: DataFrame = merged_df.drop(columns=[f"{col}_replace"])
                df: DataFrame = merged_df

            df: DataFrame = df[sorted(df.columns, key=sort_column_names)]
            df.to_csv(path_or_buf=file_path, index=False)

    def _compute_formants_at_step(self, step: str, file_names: Set[str]) -> None:
        logger.info(msg=f"Formant extraction is in progress at step: {step}")
        step_static_df, step_dynamic_df = DataFrame(), DataFrame()  # type: DataFrame
        for f in file_names:
            segments: List[Segment] = self._forced_aligner.read_textgrid(
                textgrid_file_path=join(SPEECH_DIRECTORY_PATH, step, f"{f}.TextGrid"))
            static_df: DataFrame = self._formant_extractor.get_static_formants(
                step=step, vowels=self._static_vowels, time_points=self._static_time_points,
                segments=segments, audio_file_path=join(SPEECH_DIRECTORY_PATH, step, f"{f}.wav"))
            dynamic_df: DataFrame = self._formant_extractor.get_dynamic_formants(
                step=step, vowels=self._dynamic_vowels, time_points=self._dynamic_time_points,
                segments=segments, audio_file_path=join(SPEECH_DIRECTORY_PATH, step, f"{f}.wav"))

            if not static_df.empty:
                step_static_df: DataFrame = concat(objs=[step_static_df, static_df], axis=0)
            if not dynamic_df.empty:
                step_dynamic_df: DataFrame = concat(objs=[step_dynamic_df, dynamic_df], axis=0)

        self._update_formants_file(df=step_static_df, file_path=STATIC_FORMANTS_FILE_PATH)
        self._update_formants_file(df=step_dynamic_df, file_path=DYNAMIC_FORMANTS_FILE_PATH)
        logger.info(msg=f"Formant extraction completed at step: {step}")

    def _plot_vowel_spaces_at_step(self, step: int) -> None:
        StaticVowelSpace(intermediate_steps=self._intermediate_steps, point_vowels=self._point_vowels,
                         vowel_labels=self._vowel_labels,
                         x_axis_title=self._x_axis_title, y_axis_title=self._y_axis_title,
                         x_axis_range=self._x_axis_range, y_axis_range=self._y_axis_range,
                         figure_template=self._figure_template, figure_height=self._figure_height,
                         figure_width=self._figure_width).plot(step=step)
        DynamicVowelSpace(intermediate_steps=self._intermediate_steps, time_points=self._dynamic_time_points,
                          point_vowels=self._point_vowels, vowel_labels=self._vowel_labels,
                          x_axis_title=self._x_axis_title, y_axis_title=self._y_axis_title,
                          x_axis_range=self._x_axis_range, y_axis_range=self._y_axis_range,
                          figure_template=self._figure_template, figure_height=self._figure_height,
                          figure_width=self._figure_width).plot(step=step)

    def process_ground_truth(self, ground_truth_src_dir_path: str, only_compute_formants: bool = False) -> None:
        logger.info(msg=f"Execution started at step: {GROUND_TRUTH_DIRECTORY_NAME}")
        if not only_compute_formants:
            # Ensure the source ground truth directory exists
            if not isdir(ground_truth_src_dir_path):
                raise FileNotFoundError(f"Ground truth directory doesn't exist at {ground_truth_src_dir_path}")

            # Remove the local ground truth directory if it already exists
            if exists(path=GROUND_TRUTH_DIRECTORY_PATH):
                rmtree(path=GROUND_TRUTH_DIRECTORY_PATH)
            makedirs(name=GROUND_TRUTH_DIRECTORY_PATH)  # Create a new ground truth directory

            _ground_truth_file_names: List[str] = listdir(path=ground_truth_src_dir_path)
            # Identify filenames that have both .txt and .wav extensions
            _txt_files: Set[str] = {splitext(p=f)[0] for f in _ground_truth_file_names if f.endswith(".txt")}
            _wav_files: Set[str] = {splitext(p=f)[0] for f in _ground_truth_file_names if f.endswith(".wav")}
            file_names: Set[str] = _txt_files.intersection(_wav_files)
            # Copy only the matching .txt and .wav files
            for f in file_names:
                copy(src=join(ground_truth_src_dir_path, f"{f}.txt"), dst=join(GROUND_TRUTH_DIRECTORY_PATH, f"{f}.txt"))
                copy(src=join(ground_truth_src_dir_path, f"{f}.wav"), dst=join(GROUND_TRUTH_DIRECTORY_PATH, f"{f}.wav"))

            self._align_speech_at_step(step=GROUND_TRUTH_DIRECTORY_NAME, file_names=file_names)
        else:
            file_names: Set[str] = {splitext(p=f)[0]
                                    for f in listdir(path=GROUND_TRUTH_DIRECTORY_PATH) if f.endswith(".txt")}
        self._compute_formants_at_step(step=GROUND_TRUTH_DIRECTORY_NAME, file_names=file_names)
        logger.info(msg=f"Execution completed at step: {GROUND_TRUTH_DIRECTORY_NAME}")

    def execute(self, step: int) -> None:
        if step in self._intermediate_steps:
            logger.info(msg=f"Execution started at step: {step}")
            step_directory_path: str = join(SPEECH_DIRECTORY_PATH, step.__str__())
            # Remove the step directory if it already exists
            if exists(path=step_directory_path):
                rmtree(path=step_directory_path)
            makedirs(name=step_directory_path)  # Create a new directory for the step

            file_names: Set[str] = {splitext(p=f)[0] for f in listdir(path=TEXT_DIRECTORY_PATH) if f.endswith(".txt")}
            self._synthesize_at_step(step=step, file_names=file_names)
            self._align_speech_at_step(step=step.__str__(), file_names=file_names)
            self._compute_formants_at_step(step=step.__str__(), file_names=file_names)
            self._plot_vowel_spaces_at_step(step=step)

            # Remove the source vowel space directory if it already exists
            if exists(path=self._vowel_space_dst_dir_path):
                rmtree(path=self._vowel_space_dst_dir_path)
            copytree(src=VOWEL_SPACE_DIRECTORY_PATH, dst=self._vowel_space_dst_dir_path)
            logger.info(msg=f"Updated vowel space(s) at step: {step}")
            logger.info(msg=f"Execution completed at step: {step}")
