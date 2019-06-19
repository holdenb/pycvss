import subprocess


def execute(cmd_: list):
        """
        Executes a subprocess command
        Arguments:
        cmd {list} -- List of arguments to forward to the process

        Raises:
        subprocess.CalledProcessError:
        """
        popen = subprocess.Popen(cmd_, stdout=subprocess.PIPE, universal_newlines=True)

        for stdout_line in iter(popen.stdout.readline, ""):
                yield stdout_line 

        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
                 raise subprocess.CalledProcessError(return_code, cmd_)