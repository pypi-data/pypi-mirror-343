JOB_NO_RESULT_TERMINAL_STATES = {
    "FAILED_VALIDATION",
    "CANCELED",
    "TERMINATED",
    "NOT_ENOUGH_FUNDS",
    "JOBS_LIMIT_EXCEEDED",
}
JOB_RESULTS_READY_STATES = {"COMPLETED"}
JOB_TERMINAL_STATES = JOB_RESULTS_READY_STATES.union(JOB_NO_RESULT_TERMINAL_STATES)
JOB_NON_TERMINAL_STATES = {"PENDING", "QUEUED", "RUNNING"}
JOB_STATES = JOB_NON_TERMINAL_STATES.union(JOB_TERMINAL_STATES)

DEVICE_TYPES = {
    "cpu",
    "gpu",
    "quantum",
    "tensor-network",
    "pennylane.cpu",
    "pennylane.gpu",
    "pennylane.cpu.adjoint",
    "pennylane.gpu.adjoint",
    "mps.cpu",  # Dec 2024
    "mps.gpu",
    "pauli-path",  # Dec 2024
}

MAXIMUM_NUMBER_OF_BATCH_JOBS = 500

QUEUED_CPU_JOBS_LIMIT = 5

MAXIMUM_NUMBER_OF_JOBS_FOR_RUN = 50

MAX_QUBITS_WITH_STATEVEC = 16

MAXIMUM_NUMBER_OF_SHOTS = dict.fromkeys(DEVICE_TYPES, 100_000)
MAXIMUM_NUMBER_OF_SHOTS["mps.cpu"] = 1_000_000
MAXIMUM_NUMBER_OF_SHOTS["mps.gpu"] = 1_000_000

# Maximum size in bytes for serialized circuit data
MAXIMUM_SERIALIZED_CIRCUIT_SIZE = 10_000_000  # 10 MB
