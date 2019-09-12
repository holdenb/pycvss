
import argparse

from pycvss.service.serviceManager import ServiceManager


###############################################################################
def get_args() -> dict:
    """Get arguments from the parser

    Returns:
        dict -- Dictionary containing arguments
    """
    parser = argparse.ArgumentParser(
        description='Runs a specific service offered by the service management module.')
    parser.add_argument('-s', '--service', type=ServiceManager.ServiceType, choices=list(ServiceManager.ServiceType),
                        help="The name of the service which should be instanciated for video processing.")
    parser.add_argument('-i', '--input', type=str, default=None,
                        help="Path to the input video that will be processed with the selected service.")
    parser.add_argument('-o', '--output', type=str, default=None,
                        help="Path to (and including) the output video file that will be created from processing.")

    return parser.parse_args()


###############################################################################
if __name__ == "__main__":
    args = get_args()
    sm = ServiceManager(args.service)
    print(f"Service created of type: {sm.type}")
