import os
import subprocess
import time 
import math 


######################################################################################
# Utility functions


def dec_calculate_time(func_):
        """Decorator for benchmarking a single function call

        example call:
        @dec_calculate_time
        def my_funct():
                pass

        Arguments:
        func {function} -- Function to benchmark

        Returns:
        function -- The decorated function
        """
        def decorated(*args, **kwargs):
                """Inner function to be decorated"""
                begin = time.time()
                func_(*args, **kwargs)
                end = time.time()
                
                return (end - begin)

        return decorated


def dec_exec_output_stream(func_):
        """Decorator for executing a subprocess argument list
        returned from a given decorated function. This decorator
        will also print stdout to the console.

        example call:
        @dec_exec_output_stream
        def my_funct():
                return args

        Arguments:
        func {function} -- Function that returns arguments
                that we should execute and then print process
                stdout

        Returns:
        function -- The decorated function
        """
        def decorated(*args, **kwargs):
                """Inner function to be decorated"""
                args_base = func_(*args, **kwargs)
                for path in execute(args_base):
                        print(path, end="")

        return decorated


def execute(cmd_: list):
        """Executes a subprocess command
        
        Arguments:
        cmd {list} -- List of arguments to forward to the process

        Raises:
        subprocess.CalledProcessError
        """
        popen = subprocess.Popen(cmd_, stdout=subprocess.PIPE, universal_newlines=True)

        for stdout_line in iter(popen.stdout.readline, ""):
                yield stdout_line 

        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
                 raise subprocess.CalledProcessError(return_code, cmd_)
