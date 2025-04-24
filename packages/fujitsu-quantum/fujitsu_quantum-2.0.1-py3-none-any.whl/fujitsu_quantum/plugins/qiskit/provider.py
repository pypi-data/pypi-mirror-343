# (C) 2024 Fujitsu Limited

from typing import List

from fujitsu_quantum.devices import Devices
from fujitsu_quantum.plugins.qiskit.backend import FujitsuBackend


class FujitsuProvider:

    def __init__(self):
        super().__init__()
        devices = Devices.list()
        self._backends: List[FujitsuBackend] = [FujitsuBackend(self, device) for device in devices]

    def backend(self, name: str) -> FujitsuBackend:
        for backend in self._backends:
            if backend.name == name:
                return backend

        raise ValueError(f'No such backend: {name}')
