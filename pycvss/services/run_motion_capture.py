import os
import sys
import pycvss.ffmpeg.fdcm as fdcm
import pycvss.sample_files as sample_files


OUTPUT_DIR = os.path.dirname(sys.argv[0]) + os.sep + 'output_dir'


###############################################################################
if __name__ == "__main__":
    # Testing the FDCM detector
    fdcm_detector = fdcm.Fdcm()
    fdcm_detector.input_file = sample_files.SAMPLE_VIDEO_BRIDGE
    fdcm_detector.output_dir = OUTPUT_DIR
    fdcm_detector.process()
