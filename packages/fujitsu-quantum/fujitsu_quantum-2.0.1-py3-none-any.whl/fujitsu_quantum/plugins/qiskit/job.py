# (C) 2024 Fujitsu Limited

from __future__ import annotations

import typing
from typing import Any, Dict, List, Optional, cast

from qiskit import QuantumCircuit, qasm3
from qiskit.providers import JobStatus, JobV1
from qiskit.result import Result

from fujitsu_quantum.tasks import Task

if typing.TYPE_CHECKING:
    from fujitsu_quantum.plugins.qiskit.backend import FujitsuBackend


class FujitsuJob(JobV1):

    _STATUS_MAP: Dict[Task.Status, JobStatus] = {
        Task.Status.QUEUED: JobStatus.QUEUED,
        Task.Status.RUNNING: JobStatus.RUNNING,
        Task.Status.CANCELLING: JobStatus.RUNNING,
        Task.Status.COMPLETED: JobStatus.DONE,
        Task.Status.FAILED: JobStatus.ERROR,
        Task.Status.CANCELLED: JobStatus.CANCELLED
    }

    def __init__(self,
                 backend: FujitsuBackend,
                 circuits: List[QuantumCircuit],
                 **options):
        super().__init__(backend, job_id='n/a')  # The job ID will be determined by the cloud backend later

        if typing.TYPE_CHECKING:
            self._backend: FujitsuBackend = cast(FujitsuBackend, self._backend)

        self._circuits = circuits
        self._options: Dict[str, Any] = options

        # Regard shots as n_shots for Fujitsu Quantum Cloud
        if ((self._options['shots'] is not None)
                and (self._options['n_shots'] is not None)
                and (self._options['shots'] != self._options['n_shots'])):
            raise ValueError(f'Illegal (n_)shots parameters. shots={self._options["shots"]} whereas n_shots={self._options["n_shots"]}. Please specify only one of the two.')

        # Regard seed_simulator as seed_simulation for Fujitsu Quantum Cloud
        if ((self._options['seed_simulator'] is not None)
                and (self._options['seed_simulation'] is not None)
                and (self._options['seed_simulator'] != self._options['seed_simulation'])):
            raise ValueError(f'Illegal seed for simulation. seed_simulator={self._options["seed_simulator"]} whereas seed_simulation={self._options["seed_simulation"]}. Please specify only one of the two.')

        self._fqc_options: Dict[str, Any] = options.copy()
        self._fqc_options['n_shots'] = self._fqc_options['shots']

        self._task: Optional[Task] = None
        self._result: Optional[Result] = None

    def submit(self):
        programs = list(map(lambda c: qasm3.dumps(c), self._circuits))
        self._task = self._backend.device.submit_sampling_task(programs, **self._fqc_options)
        self._job_id = str(self._task.task_id)

    def result(self) -> Result:
        if self._result is None:
            self._result = self._get_result()

        return self._result

    @staticmethod
    def _create_experiment_header(circuit: QuantumCircuit) -> dict:
        clbit_labels = []
        creg_sizes = []
        memory_slots = 0
        for creg in circuit.cregs:
            for i in range(creg.size):
                clbit_labels.append([creg.name, i])
            creg_sizes.append([creg.name, creg.size])
            memory_slots += creg.size

        qubit_labels = []
        qreg_sizes = []
        num_qubits = 0
        for qreg in circuit.qregs:  # 'qregs' includes ancilla registers
            for i in range(qreg.size):
                qubit_labels.append([qreg.name, i])
            qreg_sizes.append([qreg.name, qreg.size])
            num_qubits += qreg.size

        header = {
            'clbit_labels': clbit_labels,
            'creg_sizes': creg_sizes,
            'global_phase': float(circuit.global_phase),
            'memory_slots': memory_slots,
            'metadata': circuit.metadata,
            'n_qubits': num_qubits,
            'name': circuit.name,
            'qreg_sizes': qreg_sizes,
            'qubit_labels': qubit_labels,
        }

        return header

    def _get_result(self) -> Result:
        fqc_result  = self._task.result()

        exp_result_list = []
        for i, circuit in enumerate(self._circuits):
            if fqc_result.task_status == Task.Status.COMPLETED:
                data = { hex(int(bit_string, 2)): count for bit_string, count in fqc_result[i].counts.items() }
                exp_result_data = {'counts': data}
            else:
                exp_result_data = {}

            exp_result = {
                'shots': self._fqc_options.get('n_shots', None),
                'success': fqc_result.task_status == Task.Status.COMPLETED,
                'data': exp_result_data,
                'status': fqc_result.task_status,
                'header': self._create_experiment_header(circuit),  # required by some Qiskit methods (e.g., Result.get_counts())
            }
            exp_result_list.append(exp_result)

        return Result.from_dict({
            'backend_name': self._backend.name,
            'backend_version': self._backend.backend_version,
            'job_id': self._job_id,
            'success': fqc_result.task_status == Task.Status.COMPLETED,
            'results': exp_result_list,
            'status': fqc_result.task_status,
            'header': { 'fqc_task': self._task },
        })

    def cancel(self):
        self._task.cancel()

    def delete(self):
        self._task.delete()

    def status(self) -> JobStatus:
        return self._STATUS_MAP[self._task.status]
