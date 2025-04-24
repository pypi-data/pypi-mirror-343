from sapiopycommons.ai.api.plan.tool.proto import entry_pb2 as _entry_pb2
from sapiopycommons.ai.api.plan.proto import step_pb2 as _step_pb2
from sapiopycommons.ai.api.session.proto import sapio_conn_info_pb2 as _sapio_conn_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepCsvHeaderRow as StepCsvHeaderRow
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepCsvRow as StepCsvRow
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepCsvData as StepCsvData
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepJsonData as StepJsonData
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepTextData as StepTextData
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepBinaryData as StepBinaryData
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepImageData as StepImageData
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepEntryData as StepEntryData
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepEntryInputData as StepEntryInputData
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepEntryOutputData as StepEntryOutputData
from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import DataType as DataType
from sapiopycommons.ai.api.plan.proto.step_pb2 import StepIoInfo as StepIoInfo
from sapiopycommons.ai.api.plan.proto.step_pb2 import StepIoDetails as StepIoDetails
from sapiopycommons.ai.api.plan.proto.step_pb2 import StepInputDetails as StepInputDetails
from sapiopycommons.ai.api.plan.proto.step_pb2 import StepOutputDetails as StepOutputDetails
from sapiopycommons.ai.api.session.proto.sapio_conn_info_pb2 import SapioConnectionInfo as SapioConnectionInfo
from sapiopycommons.ai.api.session.proto.sapio_conn_info_pb2 import SapioUserSecretType as SapioUserSecretType

DESCRIPTOR: _descriptor.FileDescriptor
BINARY: _entry_pb2.DataType
JSON: _entry_pb2.DataType
CSV: _entry_pb2.DataType
TEXT: _entry_pb2.DataType
IMAGE: _entry_pb2.DataType
SESSION_TOKEN: _sapio_conn_info_pb2.SapioUserSecretType
PASSWORD: _sapio_conn_info_pb2.SapioUserSecretType

class JobStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PENDING: _ClassVar[JobStatus]
    RUNNING: _ClassVar[JobStatus]
    COMPLETED: _ClassVar[JobStatus]
    FAILED: _ClassVar[JobStatus]
PENDING: JobStatus
RUNNING: JobStatus
COMPLETED: JobStatus
FAILED: JobStatus

class CreateScriptJobRequest(_message.Message):
    __slots__ = ("sapio_user", "script_language", "plan_instance_id", "step_instance_id", "invocation_id", "input_configs", "output_configs", "script", "timeout", "max_memory_mb", "working_directory", "entry_data")
    SAPIO_USER_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    PLAN_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    STEP_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    INVOCATION_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    MAX_MEMORY_MB_FIELD_NUMBER: _ClassVar[int]
    WORKING_DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    ENTRY_DATA_FIELD_NUMBER: _ClassVar[int]
    sapio_user: _sapio_conn_info_pb2.SapioConnectionInfo
    script_language: str
    plan_instance_id: int
    step_instance_id: int
    invocation_id: int
    input_configs: _containers.RepeatedCompositeFieldContainer[_step_pb2.StepIoInfo]
    output_configs: _containers.RepeatedCompositeFieldContainer[_step_pb2.StepIoInfo]
    script: str
    timeout: int
    max_memory_mb: int
    working_directory: str
    entry_data: _containers.RepeatedCompositeFieldContainer[_entry_pb2.StepEntryInputData]
    def __init__(self, sapio_user: _Optional[_Union[_sapio_conn_info_pb2.SapioConnectionInfo, _Mapping]] = ..., script_language: _Optional[str] = ..., plan_instance_id: _Optional[int] = ..., step_instance_id: _Optional[int] = ..., invocation_id: _Optional[int] = ..., input_configs: _Optional[_Iterable[_Union[_step_pb2.StepIoInfo, _Mapping]]] = ..., output_configs: _Optional[_Iterable[_Union[_step_pb2.StepIoInfo, _Mapping]]] = ..., script: _Optional[str] = ..., timeout: _Optional[int] = ..., max_memory_mb: _Optional[int] = ..., working_directory: _Optional[str] = ..., entry_data: _Optional[_Iterable[_Union[_entry_pb2.StepEntryInputData, _Mapping]]] = ...) -> None: ...

class CreateScriptJobResponse(_message.Message):
    __slots__ = ("job_id",)
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class GetJobRequest(_message.Message):
    __slots__ = ("job_id", "log_offset")
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    LOG_OFFSET_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    log_offset: int
    def __init__(self, job_id: _Optional[str] = ..., log_offset: _Optional[int] = ...) -> None: ...

class GetJobResponse(_message.Message):
    __slots__ = ("status", "log", "exception", "entry_data")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LOG_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    ENTRY_DATA_FIELD_NUMBER: _ClassVar[int]
    status: JobStatus
    log: str
    exception: str
    entry_data: _containers.RepeatedCompositeFieldContainer[_entry_pb2.StepEntryOutputData]
    def __init__(self, status: _Optional[_Union[JobStatus, str]] = ..., log: _Optional[str] = ..., exception: _Optional[str] = ..., entry_data: _Optional[_Iterable[_Union[_entry_pb2.StepEntryOutputData, _Mapping]]] = ...) -> None: ...
