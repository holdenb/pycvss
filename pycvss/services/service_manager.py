import imageio
from abc import ABC, abstractmethod
from arghandler import *

import pycvss.ffmpeg.fdcm as fdcm
import pycvss.ssd.detect as detect
from pycvss.ffmpeg.bindings import *
from pycvss.ffmpeg.calls import *
from pycvss.utils import check_filepath, dec_singleton


###############################################################################
# Helper functions

def add_parse_filepath(parser_, arg_: str,
                       arg_context_: str, help_: str=None) -> None:
    """Add a convenient option for parsing a filepath.

    Arguments:
        parser_ {Argparser} -- Argument parser
        arg_ {str} -- Argument name
        arg_context_ {str} -- Argument context

    Keyword Arguments:
        help_ {str} -- Help string for this argument (default: {None})
    """
    if '-' not in arg_ or '--' not in arg_context_:
        raise Exception('Invalid argument or context argument.')
    parser_.add_argument(
            arg_, arg_context_, type=str,
            default=None, required=True, help=help_
    )


def validate_file(input_file_: str, name_: str) -> None:
    """Validate that a file exists & is a file.

    Arguments:
        input_file_ {str} -- Input filepath
        name_ {str} -- Name of the argument in which this file correlates
        to
    """
    if not check_filepath(input_file_):
        raise FileNotFoundError(f'{name_} is invalid or not found.')


###############################################################################
class Service(ABC):
    """Base service interface from which subclasses should implement. This
    Object provides a process method. The process method will translate directly
    into a sub-argument on the manager. Subclasses should implement _process
    and _run_service to define a way arguments are processed / displayed and
    an entry point into service execution.
    """
    def __init__(self, type_: str, command_context_: dict):
        """
        Arguments:
            type_ {str} -- Service type (name)
            command_context_ {dict} -- Command context from the manager
        """
        super().__init__()
        self.type = type_
        command_context_.update({self.type: self.process})

    def process(self, parser_, context_, args_) -> None:
        """This method will be directly translated into a sub-argument on
        the manager. It will use the name of the service as the argument name.
        This method will process arguments from the child class,
        and then pass those arguments to an overridden _run_service method.

        Arguments:
            parser_ {ArgumentParser} -- Argument parser
            context_ {parser context object} -- Parser context
            args_ {dict context} -- Parser arguments
        """
        # Process arguments and feed them to the service execution
        self._process(parser_, context_, args_)
        args_ = parser_.parse_args(args_)
        self._run_service(args_)

    @abstractmethod
    def _process(self, parser_, context_, args_) -> None:
        """Defines a way to create and process arbitrary
        arguments. Arguments need to be added to the
        parser within this method. The base service will
        handle the parsing and passing of the arguments to the
        _run_service method.

        Arguments:
            parser_ {ArgumentParser} -- Argument parser
            context_ {parser context object} -- Parser context
            args_ {dict context} -- Parser arguments
        """

    @abstractmethod
    def _run_service(self, args_) -> None:
        """Defines a way to run a service. Service core
        code should be implemented through this method.
        args_ should be fully populated with values parsed
        from the defined arguments within the _process method.

        Arguments:
            args_ {dict context} -- Populated parser arguments
        """


###############################################################################
class MotionCaptureService(Service):
    """Motion capture service object

    Ex call:
    py run_service.py motioncapture
        -i ..\..\data\sample_video\paris_people_bridge00_preview.mp4
        -o output.mp4
    """
    def __init__(self, command_context: dict):
        super().__init__('motioncapture', command_context)

    def _process(self, parser_, context_, args_) -> None:
        add_parse_filepath(
            parser_, '-i', '--input',
            help_='Input file that will be processed.'
        )
        add_parse_filepath(
            parser_, '-o', '--output',
            help_='Output directory for captured motion.'
        )

    def _run_service(self, args_) -> None:
        input_file = args_.input
        validate_file(input_file, 'Input file')

        output_dir = args_.output

        fdcm_detector = fdcm.Fdcm()
        fdcm_detector.input_file = input_file
        fdcm_detector.output_dir = output_dir
        fdcm_detector.process()


class ClassificationService(Service):
    """Classification service object

    Ex call:
    py run_service.py classification
        -i ..\..\data\sample_video\paris_people_bridge00_preview.mp4
        -o output.mp4
        -pth ..\..\..\ssd300_mAP_77.43_v2.pth
    """
    def __init__(self, command_context: dict):
        super().__init__('classification', command_context)

    def _process(self, parser_, context_, args_) -> None:
        add_parse_filepath(
            parser_, '-i', '--input',
            help_='Input file that will be processed.'
        )
        add_parse_filepath(
            parser_, '-o', '--output',
            help_='Output file with classified frames.'
        )
        add_parse_filepath(
            parser_, '-pth', '--training_file',
            help_='SSD Training file.'
        )

    def _run_service(self, args_) -> None:
        input_file = args_.input
        validate_file(input_file, 'Input file')

        training_file = args_.training_file
        validate_file(training_file, 'Training file')

        output_file = args_.output

        ssd_neural_net = detect.initialize_ssd(training_file)
        base_transform = detect.get_base_transform(ssd_neural_net)

        (frame_reader, fps) = detect.get_reader_fps_pair_from_stream(
            input_file)

        with imageio.get_writer(output_file, fps=fps) as frame_writer:
            for i, frame in enumerate(frame_reader):
                # Detected frame
                new_frame = detect.detect_frame(
                    frame, ssd_neural_net.eval(), base_transform)

                # Append our new detected frame to the new video writer
                frame_writer.append_data(new_frame)
                print(f'Processing frame: {i}')


class GrayscaleConversionService(Service):
    """Grayscale video conversion service

    Ex Call:

    py run_service.py grayscale
        -i ..\..\data\sample_video\paris_people_bridge00_preview.mp4
        -o output.mp4
    """
    def __init__(self, command_context: dict):
        super().__init__('grayscale', command_context)

    def _process(self, parser_, context_, args_) -> None:
        add_parse_filepath(
            parser_, '-i', '--input',
            help_='Input file that will be processed.'
        )
        add_parse_filepath(
            parser_, '-o', '--output',
            help_='Output file of the conversion.'
        )

    def _run_service(self, args_) -> None:
        call_log_args(
            lambda: grayscale_conversion_args(args_.input, args_.output))


###############################################################################
@dec_singleton
class ServiceManager:
    """Service management object.
    The service manager handles services and their sub-argument implementations.
    Each service is given a context object which will be populated with the service's
    respective "process" command. This command (sub-argument) is called with the
    name of the service. The service manager will also handle any top level arguments.
    All services registered remain alive for the lifespan of the manager.

    TODO: An idea would be to have services registerable on the manager rather
    than having them defined within here.
    """
    def __init__(self):
        # Command context that is passed to each Service
        # The command context is dictionary of all subcommands implemented by
        # each registered service.
        # NOTE keys in the command_context are the defined service names
        command_context = {}

        # List of registered services
        self.services = [
            MotionCaptureService(command_context),
            ClassificationService(command_context),
            GrayscaleConversionService(command_context)
        ]

        # List of service types that are available after services are
        # registered.
        self.service_types = list(command_context.keys())

        # Service list subcommand
        @subcmd('services')
        def cmd_services(parser_, context_, args_):
            print(self.service_types)

        # Set up the base argument handler
        # Argument handler object
        self.__handler = ArgumentHandler(enable_autocompletion=True)
        self.__handler.add_help
        self.__handler._use_subcommand_help
        # The handler will utilize the context to create subcommands for each
        # process function that is registered by the services
        self.__handler.set_subcommands(command_context)
        self.__handler.run()
