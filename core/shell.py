####################################################################
#  shell.py                                                        #
####################################################################
#                                                                  #
#                      This file is part of:                       #
#                        MOONVEIL PROJECT                          #
#                                                                  #
####################################################################

import asyncio

class AsyncShellCommand:
    def __init__(self, cmd, timeout=None):
        self.cmd = cmd
        self.proc = None
        self.stdout = None
        self.stderr = None
        self.timeout = timeout

    async def run(self):
        try:
            # Subprocess
            self.proc = await asyncio.create_subprocess_shell(
                self.cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            self.stdout, self.stderr = await asyncio.wait_for(
                self.proc.communicate(), timeout=self.timeout)
            await asyncio.wait_for(self.proc.wait(), timeout=1)

        # Timeout
        except asyncio.TimeoutError:
            try:
                self.proc.terminate()
                await asyncio.wait_for(self.proc.wait(), timeout=1)
            except asyncio.TimeoutError:
                self.proc.kill()

    def get_output(self):
        return self.stdout.decode() if self.stdout else None

    def get_error(self):
        return self.stderr.decode() if self.stderr else None

    def get_return_code(self):
        return self.proc.returncode if self.proc else None
    