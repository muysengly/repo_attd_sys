import os
from insightface.app import FaceAnalysis

# Preload the FaceAnalysis model once for all views
path_depth = "../../../"  # adjust as needed for your project structure
fa = FaceAnalysis(name="buffalo_sc", root=f"{os.getcwd()}/{path_depth}resource/utility/", providers=["CPUExecutionProvider"])
fa.prepare(ctx_id=-1, det_thresh=0.5, det_size=(320, 320))
