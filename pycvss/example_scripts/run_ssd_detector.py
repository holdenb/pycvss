import argparse
import imageio
import pycvss.sample_files as sample_files
import pycvss.ssd.detect as detect


###############################################################################
def get_args() -> dict:
    """Get arguments from the parser

    Returns:
        dict -- Dictionary containing arguments
    """
    parser = argparse.ArgumentParser(
        description='Single Shot MultiBox Detection')
    parser.add_argument('-p', '--pth', type=str, default=None,
                        help="The path to the .pth SSD training model file.")

    return parser.parse_args()


###############################################################################
if __name__ == "__main__":
    args = get_args()
    pth_file = args.pth
    if pth_file is None:
        raise FileNotFoundError(
            "A .pth training file is required to run the SSD.")

    ssd_neural_net = detect.initialize_ssd(pth_file)
    base_transform = detect.get_base_transform(ssd_neural_net)

    (frame_reader, fps) = detect.get_reader_fps_pair_from_stream(
        sample_files.SAMPLE_VIDEO_BRIDGE)

    with imageio.get_writer('output.mp4', fps=fps) as frame_writer:
        for i, frame in enumerate(frame_reader):
            # Detected frame
            new_frame = detect.detect_frame(
                frame, ssd_neural_net.eval(), base_transform)

            # Append our new detected frame to the new video writer
            frame_writer.append_data(new_frame)
            print(f'Processing frame: {i}')
