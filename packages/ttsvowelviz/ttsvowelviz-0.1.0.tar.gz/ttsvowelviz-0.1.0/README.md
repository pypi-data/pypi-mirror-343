# TTSVowelViz

**TTSVowelViz** is a tool for visualizing static and dynamic vowel spaces **during** the training of text-to-speech (
TTS) models.
This helps researchers and developers monitor the progression of vowel quality over training steps.

---

## ✨ Features

- 📊 **Visualize static and dynamic vowel spaces** across training steps.
- 📈 **Track vowel space evolution** during model training.
- 🔍 **Examine the shape** of the learned vowel space.
- 🆚 **Compare learned vowel spaces** at training steps against the ground truth.
- 🛠️ **Customize visualizations** with various user-defined inputs and configurations.
- 🧠 **Analyze, evaluate, and interpret** TTS systems.
- 🧩 **Easily integrate** into TTS training pipelines with minimal effort.

---

## 📦 Installation

Install using pip:

```bash
pip install ttsvowelviz
```

Or install the latest version from source:

```bash
git clone https://github.com/pasindu-ud/ttsvowelviz.git
cd ttsvowelviz
pip install .
```

---

## 🔧 Usage

### Basic Example

```python
from typing import List, Union

from ttsvowelviz import Synthesizer, TTSVowelViz
from ttsvowelviz.forced_aligner import ForcedAligner, WebMAUSBasicAligner
from ttsvowelviz.formant_extractor import FormantExtractor, PraatFormantExtractor


class ExampleSynthesizer(Synthesizer):
    def synthesize(self, step: int, text: str) -> str:
        # Code to generate speech from text at a given step
        return "Path to the synthesized audio file"


static_vowels: List[str] = ["3:", "6", "6:", "I", "O", "U", "e", "i:", "o:", "{", "}:"]
static_time_points: List[Union[int, float]] = [50]
point_vowels: List[str] = ["i:", "o:", "6:"]
dynamic_vowels: List[str] = ["@}", "Ae", "e:", "oI", "{I", "{O"]
dynamic_time_points: List[Union[int, float]] = [20, 50, 80]
intermediate_steps: List[int] = [0, 1000, 3000]
synthesizer: Synthesizer = ExampleSynthesizer()
forced_aligner: ForcedAligner = WebMAUSBasicAligner(language="eng-NZ")
formant_extractor: FormantExtractor = PraatFormantExtractor()
text_list: List[str] = ["Heard foot hud heed head had hard hod thought goose hid heard.",
                        "How'd hear oat hide lloyd hare aid how'd."]
ground_truth_src_dir_path: str = "Path to the ground truth directory"
vowel_space_dst_dir_path: str = "Path to the directory where vowel spaces should be saved"

tool: TTSVowelViz = TTSVowelViz(static_vowels=static_vowels, static_time_points=static_time_points,
                                point_vowels=point_vowels, dynamic_vowels=dynamic_vowels,
                                dynamic_time_points=dynamic_time_points, intermediate_steps=intermediate_steps,
                                synthesizer=synthesizer, forced_aligner=forced_aligner,
                                formant_extractor=formant_extractor, text_list=text_list,
                                ground_truth_src_dir_path=ground_truth_src_dir_path,
                                vowel_space_dst_dir_path=vowel_space_dst_dir_path)
for s in intermediate_steps:
    tool.execute(step=s)
```

---

## 📚 Citation

If you use this tool in your research, please cite:

```
@misc{ttsvowelviz2025,
  author = {Pasindu Udawatta and Jesin James and B.T. Balamurali and Catherine I. Watson and Ake Nicholas and Binu Abeysinghe},
  title = {TTSVowelViz},
  year = {2025},
  url = {https://github.com/pasindu-ud/ttsvowelviz}
}
```

---

## 📄 License

MIT License. See [`LICENSE`](https://github.com/pasindu-ud/ttsvowelviz/blob/main/LICENSE) file for details.

---