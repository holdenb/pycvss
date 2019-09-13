import os
from pathlib import Path


###############################################################################
# Defines a group of functions used to provide optimal, ease of use input
# parameters
# for ffmpeg processess

# FFMPEG input process base arguments
FFMPEG_INPUT_PROCESS_BASE = ['ffmpeg', '-y', '-i']


##############################################################################
def _validate_input(input_: str) -> None:
    input_file = Path(input_)
    if not input_file.is_file():
        raise Exception(f'Input: {input_}: is not a valid file.')


def grayscale_conversion_args(input_: str, output_name_: str) -> list:
    """Convert a video into grayscale

    Example ffmpeg command:
    ffmpeg -hide_banner -y -i input/video.mov -vf hue=s=0 -vcodec libx264
    -acodec copy -copyts -muxdelay 0 output/video.mp4

    Arguments:
        input_ {str} -- path/to/and/including/input/videoName
        output_name_ {str} -- path/to/and/including/output/videoName

    Returns:
        list -- A List of the arguments needed to make a ffmpeg subprocess call
        Note: Decorators can handle the call
    """
    _validate_input(input_)

    args_base = FFMPEG_INPUT_PROCESS_BASE
    args = [input_, '-vf', 'hue=s=0', '-vcodec', 'libx264', '-acodec', 'copy',
            '-copyts', '-muxdelay', '0', os.path.abspath(output_name_)]

    args_base.extend(args)

    return args_base


def scale_video_args(input_: str, output_name_: str, scale_: str) -> list:
    """Scale a video to a different resolution

    Example ffmpeg command:
    ffmpeg -i ppress_1080p_16-9_23-79fps.mp4 -filter:v scale=1280:720
    -c:a copy output.mp4

    Arguments:
        input_ {str} -- path/to/and/including/input/videoName
        output_name_ {str} -- path/to/and/including/output/videoName
        scale_ {str} -- Scale string ex: '1280:70'

    Returns:
        list -- A List of the arguments needed to make a ffmpeg subprocess call
        Note: Decorators can handle the call
    """
    _validate_input(input_)

    args_base = FFMPEG_INPUT_PROCESS_BASE
    args = [input_, '-filter:v', f'scale={scale_}', '-c:a', 'copy',
            os.path.abspath(output_name_)]

    args_base.extend(args)

    return args_base


def encode_and_adjust_args(
        input_: str, output_name_: str, bitrate_=None,
        fps_=None, scale_=None) -> list:
    """Encodes a video into a Matroska container, and adjusts various fields based
    on specific settings.

    Example ffmpeg commands:
    ffmpeg -i input.webm -c:a copy -c:v vp9 -b:v 1M output.mkv

    This will copy the audio from input.webm and convert the video
    to a VP9 codec with a bitrate of 1M/s, bundled up in a Matroska container.

    ffmpeg -i input.webm -c:a copy -c:v vp9 -r 30 output.mkv

    This will do the same as above, however it will force the framerate to
    30 fps.

    ffmpeg -i input.mkv -c:a copy -s 1280x720 output.mkv

    This will do the same as the first command, but will modify the video
    to 1280x720 in the output.

    Arguments:
            input_ {str} -- Input video
            output_name_ {str} -- Output path including output name

    Keyword Arguments:
            bitrate_ {int} -- Bitrate of the encoded video (default: {None})
            fps_ {int} -- Desired framerate conversion (default: {None})
            scale_ {int} -- Desired scale conversion (default: {None})

    Returns:
        list -- A List of the arguments needed to make a ffmpeg subprocess call
        Note: Decorators can handle the call
    """
    _validate_input(input_)

    args_base = FFMPEG_INPUT_PROCESS_BASE
    args = [input_, '-c:a', 'copy', '-c:v', 'vp9']
    args_base.extend(args)

    if bitrate_ and isinstance(bitrate_, int):
        args_base.extend(['-b:v', f'{bitrate_}M'])
    if fps_ and isinstance(fps_, int):
        args_base.extend(['-r', f'{fps_}'])
    if scale_ and isinstance(scale_, int):
        args_base.extend(['-s', f'hd{scale_}'])

    output = os.path.abspath(output_name_)
    args_base.extend([output])

    return args_base


def modify_stream_args(input_: str, output_name_: str,
                       cut_point_: str, duration_: int, audio_=False) -> list:
    """Copy video and audio streams and will also trim the video. -t
    sets the cut duration to be N seconds and -ss option set the
    start point of the video eg. ('00:01:00').

    Example ffmpeg commands:
    ffmpeg -i input.mkv -c:av copy -ss 00:01:00 -t 10 output.mkv

    This command will copy audio/video streams, set the cut duration
    to 10 seconds, and set the start point to trim at 1 minute.

    Arguments:
        input_ {str} -- Input video / Matroska container
        output_name_ {str} -- Output path including output name
        cut_point_ {str} -- Cut point eg. str('00:01:00')
        duration_ {int} -- Duration of the cut eg. int(10)

    Keyword Arguments:
            audio_ {bool} -- Should we also modify/cut the audio

    Returns:
        list -- A List of the arguments needed to make a ffmpeg subprocess call
        Note: Decorators can handle the call
    """
    _validate_input(input_)
    av_input = '-c:av' if audio_ else '-c:v'

    args_base = FFMPEG_INPUT_PROCESS_BASE
    args = [input_, av_input, 'copy', '-ss', f'{cut_point_}', '-t',
            f'{str(duration_)}']

    args_base.extend(args)

    output = os.path.abspath(output_name_)
    args_base.extend([output])

    return args_base


def hw_accel_encode(input_: str, output_name_: str,
                    avg_bitrate_: int, max_bitrate_: int) -> list:
    """Uses CUDA GPU hardware acceleration to encode input video streams

    Parameter notes:
            [-hwaccel cuvid] uses NVidia CUDA GPU acceleration for
            decoding (also working: dxva2)
            [-c:v h264_nvenc] uses NVidia h264 GPU Encoder
            [-pix_fmt p010le] YUV 4:2:0 10-bit
            [-c:v hevc_nvenc] uses HEVC/h265 GPU hardware encoder
            [-preset slow] HQ gpu encoding
            [-rc vbr_hq] uses RC option to enable variable bitrate
            encoding with GPU encoding
            [-qmin:v 19 -qmax:v 14] sets minimum and maximum
            quantization values (optional)
            [-b:v 6M -maxrate:v 10M] sets average (target) and maximum
            bitrate allowed for the encoder

            Example call: Encoding high quality h265/HEVC 10-bit video via GPU:

            ffmpeg.exe -hwaccel cuvid -i inmovie.mov -pix_fmt p010le
            -c:v hevc_nvenc -preset slow
            -rc vbr_hq -b:v 6M -maxrate:v 10M -c:a aac -b:a 240k outmovie.mp4

            NOTE: There are a lot more options for GPU hardware
            encoding/decoding.
            With the options above the GPU is used for DECODING and ENCODING
            – these are the most reliable GPU encoding options. This way it is
            possible to process the frames,
            for example with the -vf option.

    Returns:
        list -- A List of the arguments needed to make a ffmpeg subprocess call
    Note: Decorators can handle the call
    """
    _validate_input(input_)

    if not isinstance(avg_bitrate_, int):
        raise TypeError("Average bitrate input is not an Integer.")
    if not isinstance(max_bitrate_, int):
        raise TypeError("Max bitrate input is not an Integer.")

    args = ['ffmpeg', '-hwaccel', 'cuvid', '-i', input_, '-pix_fmt', 'p010le', '-c:v',
            'hevc_nvenc', '-preset', 'slow', '-rc', 'vbr_hq', '-b:v',
            f'{avg_bitrate_}M', '-maxrate:v', f'{max_bitrate_}M', '-c:a', 'aac',
            '-b:a', '240k']

    output = os.path.abspath(output_name_)
    args.extend([output])

    return args
