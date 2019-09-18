

from abc import ABC, abstractmethod
from arghandler import *

from pycvss.utils import dec_singleton


###############################################################################
class Service(ABC):
    def __init__(self, type_: str, command_context_: dict):
        super().__init__()
        self.type = type_
        command_context_.update({self.type: self.process})

    @staticmethod
    @abstractmethod
    def process(parser_, context_, args_) -> None:
        pass


###############################################################################
class MotionCaptureService(Service):
    def __init__(self, command_context: dict):
        super().__init__('motioncapture', command_context)

    @staticmethod
    def process(parser_, context_, args_):
        parser_.add_argument('-rmc', '--run_motion_capture', required=True)
        args_ = parser_.parse_args(args_)
        # print('%s%s%s' % (args_.run_motion_capture, ' '.join(args_),
        #       args_.run_motion_capture))


class ClassificationService(Service):
    def __init__(self, command_context: dict):
        super().__init__('classification', command_context)

    @staticmethod
    def process(parser_, context_, args_):
        parser_.add_argument('-rc', '--run_classification', required=True)
        args_ = parser_.parse_args(args_)
        # print('%s%s%s' % (args_.run_classification,
        #       ' '.join(args_), args_.run_classification))


###############################################################################
@dec_singleton
class ServiceManager:
    def __init__(self):
        # Set up the base argument handler
        # Argument handler object
        self.__handler = ArgumentHandler(enable_autocompletion=True)
        self.__handler.add_help
        self.__handler._use_subcommand_help

        # Command context that is passed to each Service
        # The command context is dictionary of all subcommands implemented by
        # each registered service.
        command_context = {}

        # List of registered services
        self.services = [
            MotionCaptureService(command_context),
            ClassificationService(command_context)
        ]

        self.__handler.set_subcommands(command_context)
        self.__handler.run()
