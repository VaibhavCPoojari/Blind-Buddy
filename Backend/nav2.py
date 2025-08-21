from functools import partial
from typing import Any, Dict, Optional, Tuple
import cv2 as cv
from inference.core.interfaces.camera.entities import (
    SourceProperties,
    VideoFrameProducer,
)
import numpy as np
from picamera2 import Picamera2
import supervision as sv
from inference.core.interfaces.stream.inference_pipeline import InferencePipeline


class Picamera2FrameProducer(VideoFrameProducer):
    def __init__(self):
        # Initialize Picamera2
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
        try:
            frame = self._camera.capture_array()
            return True, frame
        except Exception as e:
            print(f"Failed to capture frame: {e}")
            return False, None

    def release(self):
        self._camera.close()

    def isOpened(self) -> bool:
        return self._camera.is_open

    def discover_source_properties(self) -> SourceProperties:
        try:
            frame = self._camera.capture_array()
            h, w, *_ = frame.shape
            fps = 30  # Default FPS for now, as Picamera2 FPS query might differ
            return SourceProperties(
                width=w,
                height=h,
                total_frames=-1,
                is_file=False,
                fps=fps,
                is_reconnectable=False,
            )
        except Exception as e:
            raise RuntimeError(f"Error discovering source properties: {e}")

    def initialize_source_properties(self, properties: Dict[str, float]):
        pass


# Partial producer for Picamera2
picamera2_producer = partial(Picamera2FrameProducer)

# Annotators
box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()


# Custom sink to handle predictions
def my_sink(result, video_frame):
    if result.get("output_image"):
        # Display output image
        cv.imshow("Workflow Image", result["output_image"].numpy_image)
        cv.waitKey(1)
        print(result)


def main():
    # Replace with your API details
    api_key = "0LBhbr3I29h0cIorr6ye"
    workspace_name = "shri-2krws"
    workflow_id = "custom-workflow-2"

    try:
        # Initialize InferencePipeline
        inference_pipeline = InferencePipeline.init_with_workflow(
            api_key=api_key,
            workspace_name=workspace_name,
            workflow_id=workflow_id,
            video_reference=picamera2_producer,
            max_fps=30,
            on_prediction=my_sink
        )

        print("Inference pipeline started successfully.")
        inference_pipeline.start()
        inference_pipeline.join()

    except Exception as e:
        print(f"Error running inference pipeline: {e}")
    finally:
        # Cleanup
        cv.destroyAllWindows()


if __name__ == "__main__":
    main()