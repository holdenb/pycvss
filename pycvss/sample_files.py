import os


######################################################################################
# Data directory full path
DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), 'data')
# Sample video data directory
SAMPLE_VIDEO_DIR = os.path.join (DATA_DIR, 'sample_video')

# Sample video full path
# NOTE We need to have multiple copies for each benchmark because FFMPEG cannot edit existing files in-place.
SAMPLE_VIDEO_1 = os.path.join(SAMPLE_VIDEO_DIR, 'ppress_1080p_16-9_23-79fps_1.mp4')
SAMPLE_VIDEO_2 = os.path.join(SAMPLE_VIDEO_DIR, 'ppress_1080p_16-9_23-79fps_2.mp4')
SAMPLE_VIDEO_3 = os.path.join(SAMPLE_VIDEO_DIR, 'ppress_1080p_16-9_23-79fps_3.mp4')
SAMPLE_VIDEO_4 = os.path.join(SAMPLE_VIDEO_DIR, 'dogs_1080p_16-9_25-fps_1.mp4')
SAMPLE_VIDEO_5 = os.path.join(SAMPLE_VIDEO_DIR, 'Panasonic_HDC_TM_700_P_50i.mov')
