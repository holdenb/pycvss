import pycvss.ffmpeg.benchmark as benchmark
import pycvss.sample_files as sample_files
import pycvss.ffmpeg.bindings as args


###############################################################################
# Keys
OUTPUT_MP4 = 'mp4'
OUTPUT_MKV = 'mkv'
OUTPUT_NAME_GRAYSCALE = 'convert_grayscale'
OUTPUT_NAME_SCALE_VID = 'scale_video'
OUTPUT_NAME_ENCODE_ADJUST = 'encode_and_adjust'
OUTPUT_NAME_MOD_STREAM = 'modify_stream'
OUTPUT_NAME_ENCODE_HW_ACCEL = "encode_with_hw_accel"

# Output filenames
OUTPUT_FILES = {
    OUTPUT_MP4: 'output.mp4',
    OUTPUT_MKV: 'output.mkv',
}


###############################################################################
def print_sep() -> None:
    """Prints a seperator string of 100 characters"""
    print('-' * 100)


def _format_output(str_: str) -> None:
    """Formats printed output"""
    print(str_)
    print_sep()


###############################################################################
if __name__ == "__main__":
    # Test suite setup
    tests = [
        benchmark.BTest(
            OUTPUT_NAME_GRAYSCALE,
            lambda: args.grayscale_conversion_args(
                sample_files.SAMPLE_VIDEO_PPRESS,
                OUTPUT_FILES[OUTPUT_MP4]),
            input_file_=sample_files.SAMPLE_VIDEO_PPRESS,
            output_file_=OUTPUT_FILES[OUTPUT_MP4]
        ),

        benchmark.BTest(
            OUTPUT_NAME_SCALE_VID,
            lambda: args.scale_video_args(
                sample_files.SAMPLE_VIDEO_PPRESS,
                OUTPUT_FILES[OUTPUT_MP4],
                '1280:720'),
            input_file_=sample_files.SAMPLE_VIDEO_PPRESS,
            output_file_=OUTPUT_FILES[OUTPUT_MP4]
        ),

        benchmark.BTest(
            OUTPUT_NAME_ENCODE_ADJUST,
            lambda: args.encode_and_adjust_args(
                sample_files.SAMPLE_VIDEO_PPRESS,
                OUTPUT_FILES[OUTPUT_MKV],
                bitrate_=1,
                fps_=30,
                scale_=720),
            input_file_=sample_files.SAMPLE_VIDEO_PPRESS,
            output_file_=OUTPUT_FILES[OUTPUT_MKV]
        ),

        benchmark.BTest(
            OUTPUT_NAME_MOD_STREAM,
            lambda: args.modify_stream_args(
                sample_files.SAMPLE_VIDEO_DOGS,
                OUTPUT_FILES[OUTPUT_MP4],
                '00:00:02',
                5),
            input_file_=sample_files.SAMPLE_VIDEO_PPRESS,
            output_file_=OUTPUT_FILES[OUTPUT_MP4]
        ),

        benchmark.BTest(
            OUTPUT_NAME_ENCODE_HW_ACCEL,
            lambda: args.hw_accel_encode(
                sample_files.SAMPLE_VIDEO_PPRESS,
                OUTPUT_FILES[OUTPUT_MP4],
                6,
                10),
            input_file_=sample_files.SAMPLE_VIDEO_HD_MOV,
            output_file_=OUTPUT_FILES[OUTPUT_MP4]
        )
    ]

    # Process each test and capture the results
    results = list()
    for test in tests:
        results.append(test.process())

    # Output the results
    # TODO better format the output
    print('\n[----Benchmark results----]')
    print_sep()
    list(map(_format_output, results))
    print()
