import os


######################################################################################
# Data directory full path
DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), 'data')
# Sample video data directory
SAMPLE_VIDEO_DIR = os.path.join (DATA_DIR, 'sample_video')

# Sample video full path
SAMPLE_VIDEO_PPRESS = os.path.join(SAMPLE_VIDEO_DIR, 'ppress_1080p_16-9_23-79fps.mp4')
SAMPLE_VIDEO_DOGS = os.path.join(SAMPLE_VIDEO_DIR, 'dogs_1080p_16-9_25-fps.mp4')
SAMPLE_VIDEO_HD_MOV = os.path.join(SAMPLE_VIDEO_DIR, 'Panasonic_HDC_TM_700_P_50i.mov')
