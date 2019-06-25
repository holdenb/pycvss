import os
import sys
from pathlib import Path


######################################################################################
# FFMPEG input process base arguments
FFMPEG_INPUT_PROCESS_BASE = ['ffmpeg', '-y', '-i']


def scale_video_args(input_: str, output_name_: str, scale_: str) -> list:
        """Scale a video to a different resolution

        Example ffmpeg command:
        ffmpeg -i ppress_1080p_16-9_23-79fps.mp4 -filter:v scale=1280:720 -c:a copy output.mp4
        
        Arguments:
            input_ {str} -- path/to/and/including/input/videoName
            output_name_ {str} -- path/to/and/including/output/videoName
            scale_ {str} -- Scale string ex: '1280:70'

        Returns:
            list -- A List of the arguments needed to make a ffmpeg subprocess call
            Note: Decorators can handle the call
        """
        input_file = Path(input_)
        if not input_file.is_file():
                raise Exception (f'Input: {input_}: is not a valid file.')

        args_base = FFMPEG_INPUT_PROCESS_BASE
        args = [input_, '-filter:v', f'scale={scale_}', '-c:a', 'copy', os.path.abspath(output_name_)]
        args_base.extend(args)

        return args_base


def encode_and_adjust_args(input_: str, output_name_: str, bitrate_=None, fps_=None, scale_=None) -> list:
        """Encodes a video into a Matroska container, and adjusts various fields based
        on specific settings.
        
        Example ffmpeg commands:
        ffmpeg -i input.webm -c:a copy -c:v vp9 -b:v 1M output.mkv
        
        This will copy the audio from input.webm and convert the video to a VP9 codec
        with a bitrate of 1M/s, bundled up in a Matroska container.

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
        input_file = Path(input_)
        if not input_file.is_file():
                raise FileNotFoundError(f'Input: {input_}: is not a valid file.')

        args_base = FFMPEG_INPUT_PROCESS_BASE
        args = [input_, '-c:a', 'copy', '-c:v', 'vp9']
        args_base.extend(args)

        if bitrate_ and type(bitrate_) is int:
                args_base.extend(['-b:v', f'{bitrate_}M'])
        if fps_ and type(fps_) is int:
                args_base.extend(['-r', f'{fps_}'])
        if scale_ and type(scale_) is int:
                args_base.extend(['-s', f'hd{scale_}'])

        output = os.path.abspath(output_name_)
        args_base.extend([output])

        return args_base


def modify_stream_args(input_: str, output_name_: str, cut_point_: str, duration_: int, audio_=False) -> list:
        """Copy video and audio streams and will also trim the video. -t sets the cut duration
        to be N seconds and -ss option set the start point of the video eg. ('00:01:00').

        Example ffmpeg commands:
        ffmpeg -i input.mkv -c:av copy -ss 00:01:00 -t 10 output.mkv

        This command will copy audio/video streams, set the cut duration to 10 seconds, and set
        the start point to trim at 1 minute.
        
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
        input_file = Path(input_)
        if not input_file.is_file():
                raise Exception (f'Input: {input_}: is not a valid file.')

        av_input = '-c:av' if audio_ else '-c:v'
        
        args_base = FFMPEG_INPUT_PROCESS_BASE
        args = [input_, av_input, 'copy', '-ss', f'{cut_point_}', '-t', f'{str(duration_)}']
        args_base.extend(args)
        
        output = os.path.abspath(output_name_)
        args_base.extend([output])

        return args_base
