from ctypes import c_double

import nidaqmx
import numpy as np
from nidaqmx.constants import AcquisitionType, TerminalConfiguration
from nidaqmx.stream_readers import AnalogMultiChannelReader
from nidaqmx._task_modules.read_functions import _read_analog_f_64
from toon.input.device import BaseDevice


class ForceKeyboard(BaseDevice):
    shape = (2,)
    ctype = c_double

    def __init__(self, sampling_frequency=250, indices=[7, 8], **kwargs):
        super(ForceKeyboard, self).__init__(**kwargs)
        self.sampling_frequency = sampling_frequency
        self._buffer = np.empty(self.shape, dtype=c_double)
        if len(indices) > 2:
            raise ValueError('Too many indices for ForceKeyboard.')
        self._indices = indices

    def enter(self):
        # assume first NI DAQ  is the one we want
        self._device_name = nidaqmx.system.System.local().devices[0].name
        chans = [2, 9, 1, 8, 0, 10, 3, 11, 4, 12]
        sub_chans = [chans[i] for i in self._indices]
        channels = [self._device_name + ('/ai%i' % n) for n in sub_chans]
        channels = ','.join(channels)
        dev = nidaqmx.Task()
        dev.ai_channels.add_ai_voltage_chan(channels,
                                            terminal_config=TerminalConfiguration.RSE)
        dev.timing.cfg_samp_clk_timing(self.sampling_frequency,
                                       sample_mode=AcquisitionType.CONTINUOUS)
        self._reader = AnalogMultiChannelReader(dev.in_stream)
        dev.start()
        self._device = dev

    def read(self):
        # self._reader.read_one_sample(self._buffer, timeout=0.1)
        try:
            _read_analog_f_64(self._reader._handle, self._buffer, 1, 0)
        except Exception:
            return None
        # TODO: apply calibration?
        time = self.clock()
        return time, self._buffer

    def exit(self):
        self._device.stop()
        self._device.close()


if __name__ == '__main__':
    import time
    from toon.input import MpDevice

    dev = MpDevice(ForceKeyboard())

    times = []
    with dev:
        start = time.time()
        while time.time() - start < 240:
            dat = dev.read()
            if dat is not None:
                time, data = dat
                print(data)
                times.append(time)
            time.sleep(0.016)

    times = np.hstack(times)
    import matplotlib.pyplot as plt

    plt.plot(np.diff(times))
    plt.show()
