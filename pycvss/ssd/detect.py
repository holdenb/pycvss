import cv2
import imageio
import torch
from torch.autograd import Variable
import pycvss.ssd.ssd as ssd
from pycvss.ssd.data import BaseTransform
from pycvss.ssd.data import VOC_CLASSES as labelmap


######################################################################################
def initialize_ssd(pth_file_: str, test_phase_=True) -> ssd.SSD:
    """Initialize the SSD

    Arguments:
        pth_file_ {str} -- SSD PTH training file

    Keyword Arguments:
        test_phase_ {bool} -- Should this run in a test phase? (default: {True})

    Returns:
        ssd.SSD -- Initialized SSD object
    """
    phase = 'test'
    if not test_phase_:
        phase = 'train'

    # Creating the SSD neural network
    n_net = ssd.build_ssd(phase)

    # Torch will load a tensor containing these weights before it is passed to the neural network
    n_net.load_state_dict(torch.load(pth_file_, map_location=lambda storage, loc: storage))

    return n_net


def get_base_transform(n_net: ssd.SSD) -> BaseTransform:
    """Creates a base transform tensor

    Arguments:
        n_net {ssd.SSD} -- SSD neural network

    Returns:
        BaseTransform -- A base transform tensor
    """
    return BaseTransform(n_net.size, (104.0 / 256.0, 117.0 / 256.0, 123.0 / 256.0))


def get_reader_fps_pair_from_stream(input_file_: str) -> tuple:
    """Creates a pair containing a reader and the fps of a video

    Arguments:
        input_file_ {str} -- Input file to create reader from

    Returns:
        tuple -- Tuple containing the imageio reader and the fps metadata
    """
    _reader = imageio.get_reader(input_file_)
    _fps = _reader.get_meta_data()['fps']

    return (_reader, _fps)


def detect_frame(frame_, n_net_: ssd.SSD, transform_: BaseTransform):
    """Uses the SSD neural network to detect a given frame from a video

    Arguments:
        frame_ {[type]} -- The frame to detect
        n_net_ {ssd.SSD} -- The intialized SSD
        transform_ {BaseTransform} -- The SSD basetransform tensor

    Returns:
        frame_ -- The newly detected frame
    """
     # Take range from [0,2) / we do not need the channel
    (height, width) = frame_.shape[:2]
    transformed_frame_ = transform_(frame_)[0]

    # Now we need to convert the transformed_frame_ (numpy array)
    # to a torch tensor (a more advanced matrix)
    # Need to convert RBG -> GRB for the network
    x_input = torch.from_numpy(transformed_frame_).permute(2, 0, 1)  # 0, 1, 2 -> 2, 0, 1

    # Now we need to create a fake (batch) dimension before feeding into the network
    x_input = Variable(x_input.unsqueeze(0))  # Batch will always be index 0 dimension

    # X is now a torch variable
    # Feed x into the neural network
    y_output = n_net_(x_input)

    # Capture the values of the output in a tensor
    # Detections tensor contains:
    # [batch, number of classes (dog, plane, etc), num occurrence of class, (score, x0, y0, x1, y1)]
    detections_tensor = y_output.data

    # Scale will be used to normalize the dimensions, first w/h is upper left corner,
    # second w/h is lower right corner
    scale_tensor = torch.Tensor([width, height, width, height])

    # size(1) is the number of classes, we need to loop through the classes
    for i in range(detections_tensor.size(1)):
        occurrence_of_class = 0

        # While the occ of class i >= 0.6
        while detections_tensor[0, i, occurrence_of_class, 0] >= 0.6:
            # Need to mult by scale_tensor to normalize
            # pt coords, 1: will get x0-y1
            point = (detections_tensor[0, i, occurrence_of_class, 1:] * scale_tensor).numpy()

            # Convert back to numpy array to display rectangle coordinates
            # pt0-3 = x0-y1
            cv2.rectangle(frame_,
                          (int(point[0]), int(point[1])),
                          (int(point[2]), int(point[3])),
                          (255, 0, 0), 2)

            # Print the label onto the rect (dog/person/etc)
            cv2.putText(frame_,
                        labelmap[i - 1],
                        (int(point[0]), int(point[1])),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        2,
                        (255, 255, 255),
                        2,
                        cv2.LINE_AA)

            occurrence_of_class += 1

    return frame_
