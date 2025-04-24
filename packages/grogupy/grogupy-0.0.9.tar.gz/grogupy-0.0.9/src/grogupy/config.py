# Copyright (c) [2024-2025] [Laszlo Oroszlany, Daniel Pozsar]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from os import environ


class Config:
    def __init__(self, architecture: str, tqdm: str):
        self.__viz_loaded = False

        # get architecture
        if architecture.lower() == "cpu":
            self.__architecture = "CPU"
        elif architecture.lower() == "gpu":
            self.__architecture = "GPU"
        else:
            raise Exception("Unknown architecture, use CPU or GPU!")

        if self.__architecture == "CPU":
            from mpi4py import MPI

            self.__parallel_size = MPI.COMM_WORLD.Get_size()

        elif self.__architecture == "GPU":
            import cupy as cp

            self.__parallel_size = cp.cuda.runtime.getDeviceCount()

        # get tqdm
        if tqdm[0].lower() == "1" or tqdm[0].lower() == "t":
            self.__tqdm_requested = True
        else:
            self.__tqdm_requested = False

    @property
    def viz_loaded(self):
        return self.__viz_loaded

    @property
    def architecture(self):
        return self.__architecture

    @property
    def parallel_size(self):
        return self.__parallel_size

    @property
    def is_CPU(self):
        return self.__architecture == "CPU"

    @property
    def is_GPU(self):
        return self.__architecture == "GPU"

    @property
    def tqdm_requested(self):
        return self.__tqdm_requested


CONFIG = Config(
    environ.get("GROGUPY_ARCHITECTURE", "CPU"), environ.get("GROGUPY_TQDM", "TRUE")
)

if __name__ == "__main__":
    pass
