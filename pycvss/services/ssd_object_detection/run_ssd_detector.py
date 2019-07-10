import cv2
import imageio
import torch
from torch.autograd import Variable
from pycvss.ssd.data import BaseTransform, VOC_CLASSES as labelmap
from pycvss.ssd.ssd import build_ssd

print(cv2.__version__)

X = torch.rand(5, 3)
print(X)
