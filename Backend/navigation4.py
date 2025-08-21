# Import the InferencePipeline object
from inference import InferencePipeline
# Import the built in render_boxes sink for visualizing results
from inference.core.interfaces.stream.sinks import render_boxes
 
pipeline = InferencePipeline.init(
    api_key=os.getenv("ROBOFLOW_API_KEY"), # Your Roboflow API key,
    model_id="ood-pbnro-9jsex/1", # Roboflow model to use
    video_reference=0, # Path to video, device id (int, usually 0 for built in webcams), or RTSP stream url
    on_prediction=render_boxes, # Function to run after each prediction
)
pipeline.start()
pipeline.join()