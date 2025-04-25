import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

import torch
import numpy as np
from . import util
from .wholebody import Wholebody
import cv2

def draw_pose(pose, H=None, W=None, canvas=None):
    bodies = pose['bodies']
    faces = pose['faces']
    hands = pose['hands']
    candidate = bodies['candidate']
    subset = bodies['subset']
    if canvas is None:
        if H is None and W is None:
            raise ValueError("H and W must be provided if canvas is None")
        elif H is None or W is None:
            if H is None:
                H = W
            else:
                W = H
        canvas = np.zeros(shape=(H, W, 3), dtype=np.uint8)
    canvas = util.draw_bodypose(canvas, candidate, subset)
    canvas = util.draw_handpose(canvas, hands)
    canvas = util.draw_facepose(canvas, faces)
    return canvas

class DWposeDetector:
    def __init__(self, det=None, pose=None):
        self.pose_estimation = Wholebody(det=det, pose=pose)

    def __call__(self, oriImg, return_img=False):
        img = oriImg.copy()
        ori_type = type(oriImg)
        if ori_type is not np.ndarray:
            img = np.array(img)
            # convert to bgr
            if len(img.shape) == 3:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        H, W, C = img.shape
        with torch.no_grad():
            candidate, subset = self.pose_estimation(img)
            nums, keys, locs = candidate.shape
            candidate[..., 0] /= float(W)
            candidate[..., 1] /= float(H)
            body = candidate[:,:18].copy()
            body = body.reshape(nums*18, locs)
            score = subset[:,:18]
            for i in range(len(score)):
                for j in range(len(score[i])):
                    if score[i][j] > 0.3:
                        score[i][j] = int(18*i+j)
                    else:
                        score[i][j] = -1

            un_visible = subset<0.3
            candidate[un_visible] = -1

            foot = candidate[:,18:24]

            faces = candidate[:,24:92]

            hands = candidate[:,92:113]
            hands = np.vstack([hands, candidate[:,113:]])
            
            bodies = dict(candidate=body, subset=score)
            pose = dict(bodies=bodies, hands=hands, faces=faces, foot=foot)
            if return_img:
                img_out = draw_pose(pose, canvas=img.copy())
                from PIL import Image
                if isinstance(oriImg, Image.Image):
                    img_out = cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB)
                    img_out = Image.fromarray(img_out)
                return pose, img_out
            else:
                return pose

__all__ = ['DWposeDetector', 'draw_pose', 'Wholebody']