# (C) 2024 Fujitsu Limited

from copy import copy
from typing import List, Optional, Union

from qiskit import QuantumCircuit
from qiskit.circuit import Barrier, Reset, Measure
from qiskit.circuit.library import get_standard_gate_name_mapping
from qiskit.providers import BackendV2 as Backend
from qiskit.providers import Options
from qiskit.transpiler import Target

from fujitsu_quantum.devices import Device
from fujitsu_quantum.plugins.qiskit.job import FujitsuJob


class FujitsuBackend(Backend):

    _MAX_CIRCUITS = 300

    _DEFAULT_SHOTS = 1024
    _MAX_SHOTS = 1e5

    _BACKEND_VERSION = '2.0.0'

    def __init__(self,
                 provider,
                 device: Device):

        super().__init__(provider=provider,
                         name=device.device_id,
                         backend_version=FujitsuBackend._BACKEND_VERSION)

        self._device: Device = device
        self._target: Target = self._init_target()
        # There is no need to call self.options.set_validator(...) here.
        # The validation of option values will be performed in submit_sampling_task(...) and submit_estimation_task(...)

    def _init_target(self) -> Target:
        target = Target(num_qubits=self._device.n_qubits)

        gate_name_mapping = get_standard_gate_name_mapping().copy()

        # The name of the U gate in Qiskit is 'u' while that in OpenQASM is 'U'.
        # gate_name_mapping uses Qiskit-based names while self._device.basis_gates uses OpenQASM gate names.
        # For consistency, it needs to make gate_name_mapping have a mapping of 'U'.
        gate_name_mapping['U'] = gate_name_mapping['u']

        for gate in sorted(self._device.basis_gates):
            # A custom gate class for rzx90 will be added in future version. Until that, use 'cx' instead.
            if gate == 'rzx90':
                gate = 'cx'
            target.add_instruction(gate_name_mapping[gate])

        if 'barrier' in self._device.supported_instructions:
            target.add_instruction(Barrier, name='barrier')
        if 'reset' in self._device.supported_instructions:
            target.add_instruction(Reset())
        if 'measure' in self._device.supported_instructions:
            target.add_instruction(Measure())

        return target

    def __str__(self):
        return f'Backend for {self._device.device_id} (#qubits: {self.device.n_qubits}, basis gates: {self.device.basis_gates})'

    @property
    def device(self) -> Device:
        return self._device

    @property
    def target(self) -> Target:
        return self._target

    @property
    def max_circuits(self) -> Optional[int]:
        return FujitsuBackend._MAX_CIRCUITS

    @classmethod
    def _default_options(cls) -> Options:
        return Options(
            # The followings are the options that are valid for sampling tasks

            shots=None,  # alias for n_shots
            n_shots=None,
            name=None,
            note=None,
            skip_transpilation=False,
            seed_transpilation=None,
            transpilation_options=None,
            qubit_allocation=None,
            ro_error_mitigation=None,
            n_nodes=None,
            n_per_node=None,
            seed_simulator=None,  # alias for seed_simulation
            seed_simulation=None,
            svsim_optimization=None,
            include_transpilation_result=False,
        )

    def run(self, circuits: Union[QuantumCircuit, List[QuantumCircuit]], **run_options) -> FujitsuJob:
        if not isinstance(circuits, list):
            circuits = [circuits]

        valid_options = {key: value for key, value in run_options.items() if key in self.options}
        unknown_options = set(run_options) - set(valid_options)

        if unknown_options:
            raise ValueError(f'Options {unknown_options} are invalid for this backend'
                             f' (the target device is {self._device.device_id}).')

        actual_options = copy(self.options)
        actual_options.update_options(**valid_options)
        job = FujitsuJob(backend=self, circuits=circuits, **actual_options)
        job.submit()

        return job
