from service_manager import ServiceManager


###############################################################################
if __name__ == "__main__":
    # TODO Possibly segregate each service into their own files, along with
    # the option to add them to the manager at runtime. Rather than having them
    # added to the manager on initialization within code. Not exactly sure how
    # clean that would be opposed to the current functionality.
    sm = ServiceManager()
