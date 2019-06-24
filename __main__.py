import os
import ffmpeg_py.ffmpeg.process_args as fp_args
import ffmpeg_py.ffmpeg.calls as calls
import ffmpeg_py.tests.test_ffmpeg_benchmark as tests


# Benchmarking function calls
BENCHMARK_FUNCTIONS = {
    'scale_video': lambda: calls.call_log_args(lambda: fp_args.scale_video_args(
        tests.SAMPLE_VIDEO_1, 'output.mp4', '1280:720')),
    'encode_and_adjust': lambda: calls.call_log_args(lambda: fp_args.encode_and_adjust_args(
        tests.SAMPLE_VIDEO_2, 'output.mkv', bitrate_=1, fps_=30, scale_=720)),
    'modify_stream': lambda: calls.call_log_args(lambda: fp_args.modify_stream_args(
        tests.SAMPLE_VIDEO_3, 'output.mp4', '00:00:02', 5))
}


if __name__ == "__main__":
    # Benchmarking outside of pytest-benchmark

    # TODO inject a formatting function into the list comprehension when extracting calls from the benchmarking map
    list(map(lambda x: print(x + '\n'), [str(name + ': ' + str(call())) for (name, call) in BENCHMARK_FUNCTIONS.items()]))
