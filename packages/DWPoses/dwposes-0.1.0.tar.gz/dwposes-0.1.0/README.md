# DWPose

> Lightweight whole-body pose estimator (coords only) refactored from IDEA-Research/DWPose

## Install

```bash
pip install dwposes
```

## Usage

```python
from PIL import Image
from DWPoses import DWposeDetector
model = DWposeDetector()
img = Image.open("path/to/image.png", return_img=True)
pose, imgout = model.predict(img)
# imgout is a PIL image with pose drawn on it
imgout.save("openpose.png")
# pose is a dictionary with keys [bodies, hands, faces, foot]
print(pose)
```

Alternatively, you can load with `cv2` and `numpy`:
```python
import cv2
img = cv2.imread("path/to/image.png")
pose, imgout = model.predict(img)
# imgout is a numpy array with pose drawn on it, BGR format
imgout = cv2.cvtColor(imgout, cv2.COLOR_BGR2RGB)
imgout = Image.fromarray(imgout)
imgout.save("openpose.png")
```


Alternatively, you can specify the model path to the file `yolox_l.onnx` and `dw-ll_ucoco_384.onnx`:
```python
model = DWposeDetector(det="path/to/yolox_l.onnx", pose="path/to/dw-ll_ucoco_384.onnx")
pose, imgOut = model(img, return_img=True)
if isinstance(imgOut, np.ndarray):
    imgOut = cv2.cvtColor(imgOut, cv2.COLOR_BGR2RGB)
    imgOut = Image.fromarray(imgOut)
imgOut.save("openpose.png")
print(pose)
```
