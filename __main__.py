import os
import ffmpeg_py.ffmpeg.ffmpeg_bindings as bindings
import ffmpeg_py.tests.test_ffmpeg_benchmark as tests


if __name__ == "__main__":
    # Benchmarking outside of pytest-benchmark
    bindings.scale_video_args(tests.SAMPLE_VIDEO_1, 'output.mp4', '1280:720')
    bindings.encode_and_adjust_args(tests.SAMPLE_VIDEO_2, 'output.mkv', bitrate_=1, fps_=30, scale_=720)
    bindings.modify_stream_args(tests.SAMPLE_VIDEO_3, 'output.mp4', '00:00:02', 5)
