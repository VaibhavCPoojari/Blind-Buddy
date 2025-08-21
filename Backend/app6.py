from functools import partial
from typing import Any, Dict, Optional, Tuple, Union

import cv2 as cv
from inference.core.interfaces.camera.entities import (
    SourceProperties,
    VideoFrame,
    VideoFrameProducer,
)
import numpy as np
from picamera2 import Picamera2
import supervision as sv

from inference.core.interfaces.stream.inference_pipeline import InferencePipeline


class Picamera2FrameProducer(VideoFrameProducer):
    def __init__(
        self,
    ):
        self._camera = Picamera2()
        self._camera.preview_configuration.main.size = (1280, 1280)
        self._camera.preview_configuration.main.format = "RGB888"
        self._camera.preview_configuration.align()
        self._camera.configure("preview")
        self._camera.start()

    def grab(self) -> bool:
        status, _ = self._camera.capture_metadata()
        return status

    def retrieve(self) -> Tuple[bool, Optional[np.ndarray]]:
        status, frame = self._camera.capture_array()

        return status, frame

    def release(self):
        self._camera.close()

    def isOpened(self) -> bool:
        return self._camera.is_open

    def discover_source_properties(self) -> SourceProperties:
        status, frame = self._camera.capture_array()
        if not status:
            return False, None

        h, w, *_ = frame.shape

        return SourceProperties(
            width=w,
            height=h,
            total_frames=-1,
            is_file=False,
            fps=1,   
            is_reconnectable=False,
        )

    def initialize_source_properties(self, properties: Dict[str, float]):
        pass


picamera2_producer = partial(
    Picamera2FrameProducer,
)


box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()


def my_sink(result, video_frame):
    if result.get("output_image"):
        cv.imshow("Workflow Image", result["output_image"].numpy_image)
        cv.waitKey(1)
        print(result)



inference_pipeline = InferencePipeline.init_with_workflow(
    api_key="0LBhbr3I29h0cIorr6ye",
    workspace_name="shri-2krws",
    workflow_id="custom-workflow",
    video_reference=picamera2_producer,
    max_fps=30,
    on_prediction=my_sink
)

inference_pipeline.start()
inference_pipeline.join()