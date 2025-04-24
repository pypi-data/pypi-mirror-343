---
comments: true
---

<div align="center">
  <img src="assets/logo-trackers-violet.svg" alt="Trackers Logo" width="200" height="200">
</div>

<div align="center">

<a href="https://badge.fury.io/py/trackers"><img src="https://badge.fury.io/py/trackers.svg" alt="version"></a> <a href="https://github.com/roboflow/trackers/blob/main/LICENSE.md"><img src="https://img.shields.io/badge/license-Apache%202.0-blue" alt="license"></a> <a href="https://badge.fury.io/py/trackers"><img src="https://img.shields.io/pypi/pyversions/trackers" alt="python-version"></a>
<br>
<a href="https://colab.research.google.com/drive/1VT_FYIe3kborhWrfKKBqqfR0EjQeQNiO?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="colab"></a> <a href="https://discord.gg/GbfgXGJ8Bk"><img src="https://img.shields.io/discord/1159501506232451173?logo=discord&label=discord&labelColor=fff&color=5865f2&link=https%3A%2F%2Fdiscord.gg%2FGbfgXGJ8Bk" alt="discord"></a>

</div>

`trackers` is a unified library offering clean room re-implementations of leading multi-object tracking algorithms. Its modular design allows you to easily swap trackers and integrate them with object detectors from various libraries like `ultralytics`, `inference`, `mmdetection`, or `transformers`.


| Tracker    | Paper                                                                                                          | MOTA | Year | Status | Colab                                                                                                                                                       |
| :--------- |:---------------------------------------------------------------------------------------------------------------|:-----|:-----|:-------|:------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SORT       | [![arXiv](https://img.shields.io/badge/arXiv-1602.00763-b31b1b.svg)](https://arxiv.org/abs/1602.00763)         | 74.6 | 2016 | ✅     | [![colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1VT_FYIe3kborhWrfKKBqqfR0EjQeQNiO?usp=sharing) |
| DeepSORT   | [![arXiv](https://img.shields.io/badge/arXiv-1703.07402-b31b1b.svg)](https://arxiv.org/abs/1703.07402)         | 75.4 | 2017 | ✅     | [![colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1VT_FYIe3kborhWrfKKBqqfR0EjQeQNiO?usp=sharing) |
| ByteTrack  | [![arXiv](https://img.shields.io/badge/arXiv-2110.06864-b31b1b.svg)](https://arxiv.org/abs/2110.06864)         | 77.8 | 2021 | 🚧     | 🚧                                                                                                                                                          |
| OC-SORT    | [![arXiv](https://img.shields.io/badge/arXiv-2203.14360-b31b1b.svg)](https://arxiv.org/abs/2203.14360)         | 75.9 | 2022 | 🚧     | 🚧                                                                                                                                                          |
| BoT-SORT   | [![arXiv](https://img.shields.io/badge/arXiv-2206.14651-b31b1b.svg)](https://arxiv.org/abs/2206.14651)         | 77.8 | 2022 | 🚧     | 🚧                                                                                                                                                          |

# Installation

You can install `trackers` in a [**Python>=3.9**](https://www.python.org/) environment.

!!! example "Basic Installation"

    === "pip"
        ```bash
        pip install trackers
        ```

    === "poetry"
        ```bash
        poetry add trackers
        ```

    === "uv"
        ```bash
        uv pip install trackers
        ```

!!! example "Hardware Acceleration"

    === "CPU"
        ```bash
        pip install "trackers[cpu]"
        ```

    === "CUDA 11.8"
        ```bash
        pip install "trackers[cu118]"
        ```

    === "CUDA 12.4"
        ```bash
        pip install "trackers[cu124]"
        ```

    === "CUDA 12.6"
        ```bash
        pip install "trackers[cu126]"
        ```

    === "ROCm 6.1"
        ```bash
        pip install "trackers[rocm61]"
        ```

    === "ROCm 6.2.4"
        ```bash
        pip install "trackers[rocm624]"
        ```

# Quickstart

With a modular design, `trackers` lets you combine object detectors from different libraries (such as `ultralytics`, `inference`, `mmdetection`, or `transformers`) with the tracker of your choice. Here's how you can use `SORTTracker` with various detectors:

=== "inference"

    ```python hl_lines="2 5 12"
    import supervision as sv
    from trackers import SORTTracker
    from inference import get_model

    tracker = SORTTracker()
    model = get_model(model_id="yolov11m-640")
    annotator = sv.LabelAnnotator(text_position=sv.Position.CENTER)

    def callback(frame, _):
        result = model.infer(frame)[0]
        detections = sv.Detections.from_inference(result)
        detections = tracker.update(detections)
        return annotator.annotate(frame, detections, labels=detections.tracker_id)

    sv.process_video(
        source_path="input.mp4",
        target_path="output.mp4",
        callback=callback,
    )
    ```

=== "RF-DETR"

    ```python hl_lines="2 5 11"
    import supervision as sv
    from trackers import SORTTracker
    from rfdetr import RFDETRBase

    tracker = SORTTracker()
    model = RFDETRBase()
    annotator = sv.LabelAnnotator(text_position=sv.Position.CENTER)

    def callback(frame, _):
        detections = model.predict(frame)
        detections = tracker.update(detections)
        return annotator.annotate(frame, detections, labels=detections.tracker_id)

    sv.process_video(
        source_path="input.mp4",
        target_path="output.mp4",
        callback=callback,
    )
    ```

=== "ultralytics"

    ```python hl_lines="2 5 12"
    import supervision as sv
    from trackers import SORTTracker
    from ultralytics import YOLO

    tracker = SORTTracker()
    model = YOLO("yolo11m.pt")
    annotator = sv.LabelAnnotator(text_position=sv.Position.CENTER)

    def callback(frame, _):
        result = model(frame)[0]
        detections = sv.Detections.from_ultralytics(result)
        detections = tracker.update(detections)
        return annotator.annotate(frame, detections, labels=detections.tracker_id)

    sv.process_video(
        source_path="input.mp4",
        target_path="output.mp4",
        callback=callback,
    )
    ```

=== "transformers"

    ```python hl_lines="3 6 28"
    import torch
    import supervision as sv
    from trackers import SORTTracker
    from transformers import RTDetrV2ForObjectDetection, RTDetrImageProcessor

    tracker = SORTTracker()
    image_processor = RTDetrImageProcessor.from_pretrained("PekingU/rtdetr_v2_r18vd")
    model = RTDetrV2ForObjectDetection.from_pretrained("PekingU/rtdetr_v2_r18vd")
    annotator = sv.LabelAnnotator(text_position=sv.Position.CENTER)

    def callback(frame, _):
        inputs = image_processor(images=frame, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)

        h, w, _ = frame.shape
        results = image_processor.post_process_object_detection(
            outputs,
            target_sizes=torch.tensor([(h, w)]),
            threshold=0.5
        )[0]

        detections = sv.Detections.from_transformers(
            transformers_results=results,
            id2label=model.config.id2label
        )

        detections = tracker.update(detections)
        return annotator.annotate(frame, detections, labels=detections.tracker_id)

    sv.process_video(
        source_path="input.mp4",
        target_path="output.mp4",
        callback=callback,
    )
    ```
