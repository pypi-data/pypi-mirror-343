"""Qedma Public API"""

# pylint: disable=missing-function-docstring,missing-class-docstring,missing-module-docstring
import contextlib
import datetime
import enum
import re
from collections.abc import Generator
from typing import Annotated, Literal

import loguru
import pydantic
import qiskit.qasm3
from typing_extensions import NotRequired, TypedDict


logger = loguru.logger


class RequestBase(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        extra="ignore",
        validate_assignment=True,
        arbitrary_types_allowed=False,
    )


class ResponseBase(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        extra="ignore",
        validate_assignment=True,
        arbitrary_types_allowed=False,
    )


class JobStatus(str, enum.Enum):
    """The status of a job."""

    ESTIMATING = "ESTIMATING"
    """Job was created and QESEM is currently estimating it."""
    ESTIMATED = "ESTIMATED"
    """Job was estimated. Issue the `qedma_client.start_job()` api request to initiate the execution."""  # pylint: disable=line-too-long
    RUNNING = "RUNNING"
    """Job started running. Monitor its progress using the `qedma_client.wait_for_job_complete()` 
    method."""
    SUCCEEDED = "SUCCEEDED"
    """Job finished successfully. The user can now get the results via the `qedma_client.get_job()` 
    API with the include_results = True flag."""
    FAILED = "FAILED"
    "Job failed. Review the error message in the `job.errors` field." ""
    CANCELLED = "CANCELLED"
    "The job was cancelled by the user."

    def __str__(self) -> str:
        return self.value


class TranspilationLevel(enum.IntEnum):
    LEVEL_0 = 0
    """
    Minimal transpilation: the mitigated circuit will closely resemble the input
    circuit structurally.
    """
    LEVEL_1 = 1
    """ Prepares several alternative transpilations and chooses the one that minimizes QPU time."""


class IBMQProvider(RequestBase):
    name: Literal["ibmq"] = "ibmq"
    token_ref: str | None = None
    instance: str  # hub/group/project
    channel: str = "ibm_quantum"


_PAULI_STRING_REGEX_STR = "^[XYZ][0-9]+(,[XYZ][0-9]+)*$"
Pauli = Annotated[str, pydantic.Field(pattern=_PAULI_STRING_REGEX_STR)]


class ObservableMetadata(pydantic.BaseModel):
    """Metadata for a quantum observable."""

    description: str
    "Description of the observable"


class Observable(pydantic.RootModel[dict[Pauli, float]]):
    """A quantum observable represented as a mapping of Pauli strings to their coefficients."""

    def __iter__(self) -> Generator[Pauli, None, None]:  # type: ignore[override]
        # pydantic suggests to override __iter__ method (
        # https://docs.pydantic.dev/latest/concepts/models/#rootmodel-and-custom-root-types)
        # but __iter__ method is already implemented in pydantic.BaseModel, so we just ignore the
        # warning and hope that it works as expected (tests covers dump/load methods and iter)
        yield from iter(self.root)

    def __getitem__(self, key: Pauli) -> float:
        return self.root[key]

    def __contains__(self, key: Pauli) -> bool:
        return key in self.root

    def __len__(self) -> int:
        return len(self.root)

    def __str__(self) -> str:
        return str(self.root)

    def __repr__(self) -> str:
        return "Observable(" + repr(self.root) + ")"

    def __hash__(self) -> int:
        return hash(tuple(self.root.items()))


class ExpectationValue(ResponseBase):
    """Result of a quantum measurement, containing both the measured value and its uncertainty."""

    value: float
    "The expected value of the quantum measurement"

    error_bar: float
    "The standard error associated with the measurement"

    def __str__(self) -> str:
        return f"{self.value} ± {self.error_bar}"


class ExpectationValues(pydantic.RootModel[list[tuple[Observable, ExpectationValue]]]):
    """Collection of quantum measurement results, pairing observables with their
    measured expectation values."""

    def __iter__(self) -> Generator[tuple[Observable, ExpectationValue], None, None]:  # type: ignore[override] # pylint: disable=line-too-long
        # pydantic suggests to override __iter__ method (
        # https://docs.pydantic.dev/latest/concepts/models/#rootmodel-and-custom-root-types)
        # but __iter__ method is already implemented in pydantic.BaseModel, so we just ignore the
        # warning and hope that it works as expected (tests covers dump/load methods and iter)
        yield from iter(self.root)

    def __getitem__(self, key: int) -> tuple[Observable, ExpectationValue]:
        return self.root[key]

    def __len__(self) -> int:
        return len(self.root)

    def __str__(self) -> str:
        return "[" + ", ".join([f"{obs}: ({exp})" for obs, exp in self.root]) + "]"

    def __repr__(self) -> str:
        return (
            "ExpectationValues(["
            + ",".join([f"{repr(obs)}: {repr(exp)}" for obs, exp in self.root])
            + "])"
        )


class PrecisionMode(str, enum.Enum):
    """
    Precision mode types when executing a parameterized circuit.
    """

    JOB = "JOB"
    """ QESEM will treat the `precision` as a precision for the sum of the expectation values."""
    CIRCUIT = "CIRCUIT"
    """ QESEM will target the specified `precision` for each circuit."""

    def __str__(self) -> str:
        return self.value


class ExecutionMode(str, enum.Enum):
    """The mode of execution."""

    SESSION = "SESSION"
    """ QESEM will execute the job in a single IBM dedicated session."""
    BATCH = "BATCH"
    """ QESEM will execute the job in multiple IBM batches."""

    def __str__(self) -> str:
        return self.value


class JobOptions(RequestBase):
    """Additional options for a job request"""

    execution_mode: ExecutionMode | None = None
    """ Execution mode type. Default is BATCH"""


class CircuitOptions(RequestBase):
    """Qesem circuits circuit_options"""

    error_suppression_only: bool = False
    """ No error mitigation. This results in a much shorter but biased run. When True, the `shots`
    parameter becomes mandatory, while precision and observables will be ignored!"""
    transpilation_level: TranspilationLevel = pydantic.Field(default=TranspilationLevel.LEVEL_1)
    """ Transpilation level type"""


def _check_circuit(  # type: ignore[no-any-unimported]
    value: qiskit.QuantumCircuit | str,
) -> qiskit.QuantumCircuit:
    if isinstance(value, str):
        with contextlib.suppress(Exception):
            value = qiskit.qasm3.loads(value)

    if isinstance(value, str):
        with contextlib.suppress(Exception):
            value = qiskit.QuantumCircuit.from_qasm_str(value)

    if not isinstance(value, qiskit.QuantumCircuit):
        raise ValueError("Circuit must be a valid Qiskit QuantumCircuit or QASM string")

    return value


def _serialize_circuit(value: qiskit.QuantumCircuit) -> str:  # type: ignore[no-any-unimported]
    result = qiskit.qasm3.dumps(value)
    if not isinstance(result, str):
        raise ValueError("Failed to serialize the circuit")

    return result


class ParameterizedCircuit(RequestBase):  # type: ignore[no-any-unimported]
    circuit: qiskit.QuantumCircuit  # type: ignore[no-any-unimported]
    "The quantum circuit to be executed."

    parameters: dict[str, tuple[float, ...]] | None = None
    "Optional dictionary mapping parameter names to their values for parameterized circuits. "

    @pydantic.field_validator("circuit", mode="plain", json_schema_input_type=str)
    @classmethod
    def check_circuit(cls, value: qiskit.QuantumCircuit | str) -> qiskit.QuantumCircuit:  # type: ignore[no-any-unimported] # pylint: disable=line-too-long
        return _check_circuit(value)

    @pydantic.field_serializer("circuit", mode="plain", return_type=str)
    def serialize_circuit(self, value: qiskit.QuantumCircuit) -> str:  # type: ignore[no-any-unimported] # pylint: disable=line-too-long
        return _serialize_circuit(value)

    @pydantic.model_validator(mode="after")
    def check_parameters(self) -> "ParameterizedCircuit":
        if self.parameters is None:
            if len(set(map(str, self.circuit.parameters))) > 0:
                raise ValueError("Parameters must match the circuit parameters")
            return self

        if set(map(str, self.parameters.keys())) != set(map(str, self.circuit.parameters)):
            raise ValueError("Parameters must match the circuit parameters")

        if len(self.parameters) > 0:
            if any(
                re.search(r"[^\w\d]", p, flags=re.U)
                for p in self.parameters  # pylint: disable=not-an-iterable
            ):
                raise ValueError(
                    "Parameter names must contain only alphanumeric characters, got: "
                    f"{list(self.parameters.keys())}"
                )

            # check all parameters are of the same length
            parameter_value_lengths = set(len(v) for v in self.parameters.values())
            if len(parameter_value_lengths) > 1:
                raise ValueError("All parameter values must have the same length")

        return self


class Circuit(ParameterizedCircuit):  # type: ignore[no-any-unimported]
    """A quantum circuit configuration including the circuit itself,
    observables to measure, and execution parameters."""

    observables: tuple[Observable, ...]
    """Tuple of observables to be measured. Each observable represents a measurement 
    configuration."""

    observables_metadata: tuple[ObservableMetadata, ...] | None = None
    """Tuple of metadata for the observables. 
    Each metadata corresponds to the observable at the same index."""

    precision: float
    "Target precision for the expectation value measurements"

    options: CircuitOptions
    "Additional options for circuit execution"

    @pydantic.model_validator(mode="after")
    def check_parameters_and_observables(self) -> "Circuit":
        if self.parameters and len(self.parameters) > 0:
            # check that the number of observables is equal to the number of parameters values
            parameter_value_lengths = set(len(v) for v in self.parameters.values())
            if len(self.observables) != list(parameter_value_lengths)[0]:
                raise ValueError(
                    "Number of observables must be equal to the number of parameter values"
                )

        if self.observables_metadata is not None and len(self.observables_metadata) != len(
            self.observables
        ):
            raise ValueError(
                "The number of observable metadata items must match the number of observables"
            )

        return self

    @pydantic.field_validator("options")
    @classmethod
    def validate_error_suppression_only(cls, value: CircuitOptions) -> CircuitOptions:
        if value.error_suppression_only:
            raise ValueError("Wrong circuit type!")
        return value


class ErrorSuppressionCircuit(ParameterizedCircuit):  # type: ignore[no-any-unimported]
    shots: int
    """Amount of shots to run this circuit. Only viable when error-suppression only is True!"""

    options: CircuitOptions
    "Additional options for circuit execution"

    @pydantic.field_validator("options")
    @classmethod
    def validate_error_suppression_only(cls, value: CircuitOptions) -> CircuitOptions:
        if not value.error_suppression_only:
            raise ValueError("Wrong circuit type!")
        return value


class QPUTime(TypedDict):
    """Time metrics for quantum processing unit (QPU) usage."""

    execution: datetime.timedelta
    "Actual time spent executing the quantum circuit on the QPU"

    estimation: NotRequired[datetime.timedelta]
    "Estimated time required for QPU execution, may not be present"


class TranspiledCircuit(pydantic.BaseModel):  # type: ignore[no-any-unimported]
    """Circuit to be executed on QPU"""

    circuit: qiskit.QuantumCircuit  # type: ignore[no-any-unimported]
    """The quantum circuit after optimization, ready for execution."""

    qubit_map: dict[int, int]
    "Mapping between logical qubits in the original circuit and physical qubits on the QPU"

    num_measurement_bases: int
    "Number of different measurement bases required for this circuit"

    @pydantic.field_validator("circuit", mode="plain", json_schema_input_type=str)
    @classmethod
    def check_circuit(  # type: ignore[no-any-unimported]
        cls,
        value: qiskit.QuantumCircuit | str,
    ) -> qiskit.QuantumCircuit:
        return _check_circuit(value)

    @pydantic.field_serializer("circuit", mode="plain", return_type=str)
    def serialize_circuit(  # type: ignore[no-any-unimported]
        self,
        value: qiskit.QuantumCircuit,
    ) -> str:
        return _serialize_circuit(value)


class ExecutionDetails(ResponseBase):
    """Detailed statistics about the quantum circuit execution."""

    total_shots: int
    "Total number of times the quantum circuit was executed"

    mitigation_shots: int
    "Number of shots used for error mitigation"

    gate_fidelities: dict[str, float]
    "Dictionary mapping gate names to their measured fidelities on the QPU"

    transpiled_circuits: list[TranspiledCircuit] | None = None
    """List of circuits after optimization and mapping to the QPU architecture."""


class JobStep(pydantic.BaseModel):
    """Represents a single step in a job progress"""

    name: Annotated[str, pydantic.Field(description="The name of the step")]


class JobProgress(pydantic.BaseModel):
    """Represents job progress, i.e. a list of sequential steps"""

    steps: Annotated[
        list[JobStep],
        pydantic.Field(
            description="List of steps corresponding to JobStep values",
            default_factory=list,
        ),
    ]


class JobDetails(ResponseBase):
    """Detailed information about a quantum job, including its status, execution details,
    and results."""

    account_id: str
    "The unique identifier of the user account"

    account_email: str
    "The email address associated with the user account"

    job_id: str
    "The unique identifier of the job"

    description: str = ""
    "Optional description of the job"

    masked_account_token: str
    "Partially hidden account authentication token"

    masked_qpu_token: str
    "Partially hidden QPU access token"

    qpu_name: str
    "Name of the quantum processing unit (or simulator) being used"

    circuit: Circuit | ErrorSuppressionCircuit | None = None
    "The quantum circuit to be executed. Returns only if `include_circuit` is True"

    precision_mode: PrecisionMode | None = None
    "The precision mode used for execution. Can only be used when parameters are set."

    status: JobStatus
    "Current status of the job"

    analytical_qpu_time_estimation: datetime.timedelta | None
    "Theoretical estimation of QPU execution time"

    empirical_qpu_time_estimation: datetime.timedelta | None = None
    "Measured estimation of QPU execution time based on actual runs"

    total_execution_time: datetime.timedelta
    "Total time taken for the job execution. Includes QPU and classical processing time."

    created_at: datetime.datetime
    "Timestamp when the job was created"

    updated_at: datetime.datetime
    "Timestamp when the job was last updated"

    qpu_time: QPUTime | None
    "Actual QPU time used for execution and estimation."

    qpu_time_limit: datetime.timedelta | None = None
    "Maximum allowed QPU execution time"

    warnings: list[str] | None = None
    "List of warning messages generated during job execution"

    errors: list[str] | None = None
    "List of error messages generated during job execution"

    intermediate_results: ExpectationValues | None = None
    "Partial results obtained during job execution."

    results: ExpectationValues | list[dict[int, int]] | None = None
    "Final results of the quantum computation. Returns only if `include_results` is True"

    noisy_results: ExpectationValues | list[dict[int, int]] | None = None
    "Results without error mitigation applied."

    execution_details: ExecutionDetails | None = None
    "Information about the execution process. Includes total shots, mitigation shots, and gate fidelities."  # pylint: disable=line-too-long

    progress: JobProgress | None = None
    "Current progress information of the job. Printed automatically when calling `qedma_client.wait_for_job_complete()`."  # pylint: disable=line-too-long

    def __str__(self) -> str:
        return self.model_dump_json(indent=4)
