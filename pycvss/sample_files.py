import os


###############################################################################
# Data directory full path
DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(os.path.dirname(__file__))), 'data')

# Sample video data directory
SAMPLE_VIDEO_DIR = os.path.join(DATA_DIR, 'sample_video')

# Sample videos
SAMPLE_VIDEO_PPRESS = os.path.join(
    SAMPLE_VIDEO_DIR, 'ppress_1080p_16-9_23-79fps.mp4')
SAMPLE_VIDEO_HD_MOV = os.path.join(
    SAMPLE_VIDEO_DIR, 'Panasonic_HDC_TM_700_P_50i.mov')
SAMPLE_VIDEO_RUNNING_DOG_HD = os.path.join(
    SAMPLE_VIDEO_DIR, 'running_dog_hd.mp4')
SAMPLE_VIDEO_BRIDGE = os.path.join(
    SAMPLE_VIDEO_DIR, 'paris_people_bridge00_preview.mp4')
