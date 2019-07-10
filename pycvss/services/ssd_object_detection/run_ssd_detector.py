import cv2
import imageio
import torch
from torch.autograd import Variable
from pycvss.ssd.data import BaseTransform, VOC_CLASSES as labelmap
from pycvss.ssd.ssd import build_ssd
import pycvss.sample_files as sample_files

print(cv2.__version__)

X = torch.rand(5, 3)
print(X)

def detect(frame, n_net, transform):
    (height, width) = frame.shape[:2]  # Take range from [0,2) / we do not need the channel
    frame_t = transform(frame)[0]

    # Now we need to convert the frame_t (numpy array) to a torch tensor (a more advanced matrix)
    # Need to convert RBG -> GRB for the network
    x = torch.from_numpy(frame_t).permute(2, 0, 1)  # 0, 1, 2 -> 2, 0, 1
    # Now we need to create a fake (batch) dimension before feeding into the network
    x = Variable(x.unsqueeze(0))  # Batch will always be index 0 dimension
    # X is now a torch variable

    # Feed x into the neural network
    y = n_net(x)
    # Capture the values of the output in a tensor
    # Detections tensor contains:
    # [batch, number of classes (dog, plane, etc), num occurrence of class, (score, x0, y0, x1, y1)]
    detections_tensor = y.data

    # Scale will be used to normalize the dimensions, first w/h is upper left corner, second w/h is lower right corner
    scale_tensor = torch.Tensor([width, height, width, height])

    for i in range(detections_tensor.size(1)):  # size(1) is the number of classes, we need to loop through the classes
        occurrence_of_class = 0
        while detections_tensor[0, i, occurrence_of_class, 0] >= 0.6:  # While the occ of class i >= 0.6
            # Need to mult by scale_tensor to normalize
            # pt coords, 1: will get x0-y1
            pt = (detections_tensor[0, i, occurrence_of_class, 1:] * scale_tensor).numpy()
            # Convert back to numpy array to display rectangle coordinates
            # pt0-3 = x0-y1
            cv2.rectangle(frame, (int(pt[0]), int(pt[1])), (int(pt[2]), int(pt[3])), (255, 0, 0), 2)
            # Print the label onto the rect (dog/person/etc)
            cv2.putText(frame, labelmap[i - 1], (int(pt[0]), int(pt[1])), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255),
                        2, cv2.LINE_AA)

            occurrence_of_class += 1

    return frame


# Creating the SSD neural network
net = build_ssd('test')
# Torch will load a tensor containing these weights before it is passed to the neural network

# TODO Figure out the best way to get this path, possibly a command line arg for now, as
# the file is too large to commit
net.load_state_dict(torch.load('ssd300_mAP_77.43_v2.pth', map_location=lambda storage, loc: storage))

# Create the transformation
# Scale values specific to the ssd300... training
base_transform = BaseTransform(net.size, (104.0/256.0, 117.0/256.0, 123.0/256.0))

# Object detection on a video
reader = imageio.get_reader(sample_files.SAMPLE_VIDEO_RUNNING_DOG_HD)
# Get the fps of the video
fps = reader.get_meta_data()['fps']

writer = imageio.get_writer('output.mp4', fps=fps)
for (num_frame, f) in enumerate(reader):
    new_frame = detect(f, net.eval(), base_transform)
    writer.append_data(new_frame)  # Append our new detected frame to the new video writer
    print(num_frame)  # Number of the processed frame

writer.close()
