from sapiopycommons.ai.api.fielddefinitions.proto import velox_field_def_pb2 as _velox_field_def_pb2
from sapiopycommons.ai.api.plan.tool.proto import entry_pb2 as _entry_pb2
from sapiopycommons.ai.api.plan.proto import step_pb2 as _step_pb2
from sapiopycommons.ai.api.session.proto import sapio_conn_info_pb2 as _sapio_conn_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import FieldValidatorProto as FieldValidatorProto
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import ColorRangeProto as ColorRangeProto
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import BooleanDependentFieldEntry as BooleanDependentFieldEntry
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import SelectionDependentFieldEntry as SelectionDependentFieldEntry
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import EnumDependentFieldEntry as EnumDependentFieldEntry
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import ProcessDetailEntry as ProcessDetailEntry
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import BooleanProperties as BooleanProperties
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import DateProperties as DateProperties
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import DoubleProperties as DoubleProperties
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import IntegerProperties as IntegerProperties
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import LongProperties as LongProperties
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import ShortProperties as ShortProperties
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import SelectionProperties as SelectionProperties
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import StringProperties as StringProperties
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import SideLinkProperties as SideLinkProperties
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import PickListProperties as PickListProperties
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import ParentLinkProperties as ParentLinkProperties
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import MultiParentProperties as MultiParentProperties
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import IdentifierProperties as IdentifierProperties
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import FileBlobProperties as FileBlobProperties
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import EnumProperties as EnumProperties
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import DateRangeProperties as DateRangeProperties
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import ChildLinkProperties as ChildLinkProperties
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import ActionStringProperties as ActionStringProperties
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import ActionProperties as ActionProperties
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import AccessionProperties as AccessionProperties
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import VeloxFieldDefProto as VeloxFieldDefProto
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import VeloxFieldDefProtoList as VeloxFieldDefProtoList
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import FieldTypeProto as FieldTypeProto
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import SortDirectionProto as SortDirectionProto
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import FontSizeProto as FontSizeProto
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import TextDecorationProto as TextDecorationProto
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import StringFormatProto as StringFormatProto
from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import DoubleFormatProto as DoubleFormatProto
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
FIELD_TYPE_UNSPECIFIED: _velox_field_def_pb2.FieldTypeProto
BOOLEAN: _velox_field_def_pb2.FieldTypeProto
DOUBLE: _velox_field_def_pb2.FieldTypeProto
ENUM: _velox_field_def_pb2.FieldTypeProto
LONG: _velox_field_def_pb2.FieldTypeProto
INTEGER: _velox_field_def_pb2.FieldTypeProto
SHORT: _velox_field_def_pb2.FieldTypeProto
STRING: _velox_field_def_pb2.FieldTypeProto
DATE: _velox_field_def_pb2.FieldTypeProto
ACTION: _velox_field_def_pb2.FieldTypeProto
SELECTION: _velox_field_def_pb2.FieldTypeProto
PARENTLINK: _velox_field_def_pb2.FieldTypeProto
IDENTIFIER: _velox_field_def_pb2.FieldTypeProto
PICKLIST: _velox_field_def_pb2.FieldTypeProto
LINK: _velox_field_def_pb2.FieldTypeProto
MULTIPARENTLINK: _velox_field_def_pb2.FieldTypeProto
CHILDLINK: _velox_field_def_pb2.FieldTypeProto
AUTO_ACCESSION: _velox_field_def_pb2.FieldTypeProto
DATE_RANGE: _velox_field_def_pb2.FieldTypeProto
SIDE_LINK: _velox_field_def_pb2.FieldTypeProto
ACTION_STRING: _velox_field_def_pb2.FieldTypeProto
FILE_BLOB: _velox_field_def_pb2.FieldTypeProto
SORT_DIRECTION_UNSPECIFIED: _velox_field_def_pb2.SortDirectionProto
SORT_DIRECTION_ASCENDING: _velox_field_def_pb2.SortDirectionProto
SORT_DIRECTION_DESCENDING: _velox_field_def_pb2.SortDirectionProto
SORT_DIRECTION_NONE: _velox_field_def_pb2.SortDirectionProto
FONT_SIZE_UNSPECIFIED: _velox_field_def_pb2.FontSizeProto
FONT_SIZE_SMALL: _velox_field_def_pb2.FontSizeProto
FONT_SIZE_MEDIUM: _velox_field_def_pb2.FontSizeProto
FONT_SIZE_LARGE: _velox_field_def_pb2.FontSizeProto
TEXT_DECORATION_UNSPECIFIED: _velox_field_def_pb2.TextDecorationProto
TEXT_DECORATION_NONE: _velox_field_def_pb2.TextDecorationProto
TEXT_DECORATION_UNDERLINE: _velox_field_def_pb2.TextDecorationProto
TEXT_DECORATION_STRIKETHROUGH: _velox_field_def_pb2.TextDecorationProto
STRING_FORMAT_UNSPECIFIED: _velox_field_def_pb2.StringFormatProto
STRING_FORMAT_PHONE: _velox_field_def_pb2.StringFormatProto
STRING_FORMAT_EMAIL: _velox_field_def_pb2.StringFormatProto
DOUBLE_FORMAT_UNSPECIFIED: _velox_field_def_pb2.DoubleFormatProto
DOUBLE_FORMAT_CURRENCY: _velox_field_def_pb2.DoubleFormatProto
DOUBLE_FORMAT_PERCENTAGE: _velox_field_def_pb2.DoubleFormatProto
BINARY: _entry_pb2.DataType
JSON: _entry_pb2.DataType
CSV: _entry_pb2.DataType
TEXT: _entry_pb2.DataType
IMAGE: _entry_pb2.DataType
SESSION_TOKEN: _sapio_conn_info_pb2.SapioUserSecretType
PASSWORD: _sapio_conn_info_pb2.SapioUserSecretType

class ToolIoConfigBase(_message.Message):
    __slots__ = ("content_type", "io_number", "display_name", "description", "example")
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    IO_NUMBER_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXAMPLE_FIELD_NUMBER: _ClassVar[int]
    content_type: str
    io_number: int
    display_name: str
    description: str
    example: str
    def __init__(self, content_type: _Optional[str] = ..., io_number: _Optional[int] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., example: _Optional[str] = ...) -> None: ...

class ToolInputDetails(_message.Message):
    __slots__ = ("base_config", "validation", "min_input_count", "max_input_count", "paged", "min_page_size", "max_page_size", "max_request_bytes")
    BASE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_FIELD_NUMBER: _ClassVar[int]
    MIN_INPUT_COUNT_FIELD_NUMBER: _ClassVar[int]
    MAX_INPUT_COUNT_FIELD_NUMBER: _ClassVar[int]
    PAGED_FIELD_NUMBER: _ClassVar[int]
    MIN_PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    MAX_PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    MAX_REQUEST_BYTES_FIELD_NUMBER: _ClassVar[int]
    base_config: ToolIoConfigBase
    validation: str
    min_input_count: int
    max_input_count: int
    paged: bool
    min_page_size: int
    max_page_size: int
    max_request_bytes: int
    def __init__(self, base_config: _Optional[_Union[ToolIoConfigBase, _Mapping]] = ..., validation: _Optional[str] = ..., min_input_count: _Optional[int] = ..., max_input_count: _Optional[int] = ..., paged: bool = ..., min_page_size: _Optional[int] = ..., max_page_size: _Optional[int] = ..., max_request_bytes: _Optional[int] = ...) -> None: ...

class ToolOutputDetails(_message.Message):
    __slots__ = ("base_config",)
    BASE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    base_config: ToolIoConfigBase
    def __init__(self, base_config: _Optional[_Union[ToolIoConfigBase, _Mapping]] = ...) -> None: ...

class ProcessStepRequest(_message.Message):
    __slots__ = ("sapio_user", "tool_name", "plan_instance_id", "step_instance_id", "invocation_id", "input_configs", "output_configs", "config_field_values", "entry_data")
    class ConfigFieldValuesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: StepRecordFieldValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[StepRecordFieldValue, _Mapping]] = ...) -> None: ...
    SAPIO_USER_FIELD_NUMBER: _ClassVar[int]
    TOOL_NAME_FIELD_NUMBER: _ClassVar[int]
    PLAN_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    STEP_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    INVOCATION_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_VALUES_FIELD_NUMBER: _ClassVar[int]
    ENTRY_DATA_FIELD_NUMBER: _ClassVar[int]
    sapio_user: _sapio_conn_info_pb2.SapioConnectionInfo
    tool_name: str
    plan_instance_id: int
    step_instance_id: int
    invocation_id: int
    input_configs: _containers.RepeatedCompositeFieldContainer[_step_pb2.StepIoInfo]
    output_configs: _containers.RepeatedCompositeFieldContainer[_step_pb2.StepIoInfo]
    config_field_values: _containers.MessageMap[str, StepRecordFieldValue]
    entry_data: _containers.RepeatedCompositeFieldContainer[_entry_pb2.StepEntryInputData]
    def __init__(self, sapio_user: _Optional[_Union[_sapio_conn_info_pb2.SapioConnectionInfo, _Mapping]] = ..., tool_name: _Optional[str] = ..., plan_instance_id: _Optional[int] = ..., step_instance_id: _Optional[int] = ..., invocation_id: _Optional[int] = ..., input_configs: _Optional[_Iterable[_Union[_step_pb2.StepIoInfo, _Mapping]]] = ..., output_configs: _Optional[_Iterable[_Union[_step_pb2.StepIoInfo, _Mapping]]] = ..., config_field_values: _Optional[_Mapping[str, StepRecordFieldValue]] = ..., entry_data: _Optional[_Iterable[_Union[_entry_pb2.StepEntryInputData, _Mapping]]] = ...) -> None: ...

class ProcessStepResponse(_message.Message):
    __slots__ = ("new_records", "log", "entry_data")
    NEW_RECORDS_FIELD_NUMBER: _ClassVar[int]
    LOG_FIELD_NUMBER: _ClassVar[int]
    ENTRY_DATA_FIELD_NUMBER: _ClassVar[int]
    new_records: _containers.RepeatedCompositeFieldContainer[StepRecord]
    log: _containers.RepeatedScalarFieldContainer[str]
    entry_data: _containers.RepeatedCompositeFieldContainer[_entry_pb2.StepEntryOutputData]
    def __init__(self, new_records: _Optional[_Iterable[_Union[StepRecord, _Mapping]]] = ..., log: _Optional[_Iterable[str]] = ..., entry_data: _Optional[_Iterable[_Union[_entry_pb2.StepEntryOutputData, _Mapping]]] = ...) -> None: ...

class ToolDetailsRequest(_message.Message):
    __slots__ = ("sapio_conn_info",)
    SAPIO_CONN_INFO_FIELD_NUMBER: _ClassVar[int]
    sapio_conn_info: _sapio_conn_info_pb2.SapioConnectionInfo
    def __init__(self, sapio_conn_info: _Optional[_Union[_sapio_conn_info_pb2.SapioConnectionInfo, _Mapping]] = ...) -> None: ...

class StepRecordFieldValue(_message.Message):
    __slots__ = ("string_value", "int_value", "double_value", "bool_value")
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    string_value: str
    int_value: int
    double_value: float
    bool_value: bool
    def __init__(self, string_value: _Optional[str] = ..., int_value: _Optional[int] = ..., double_value: _Optional[float] = ..., bool_value: bool = ...) -> None: ...

class StepRecord(_message.Message):
    __slots__ = ("fields",)
    class FieldsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: StepRecordFieldValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[StepRecordFieldValue, _Mapping]] = ...) -> None: ...
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.MessageMap[str, StepRecordFieldValue]
    def __init__(self, fields: _Optional[_Mapping[str, StepRecordFieldValue]] = ...) -> None: ...

class ToolDetails(_message.Message):
    __slots__ = ("name", "description", "output_data_type_name", "input_configs", "output_configs", "config_fields")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_DATA_TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    INPUT_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELDS_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    output_data_type_name: str
    input_configs: _containers.RepeatedCompositeFieldContainer[ToolInputDetails]
    output_configs: _containers.RepeatedCompositeFieldContainer[ToolOutputDetails]
    config_fields: _containers.RepeatedCompositeFieldContainer[_velox_field_def_pb2.VeloxFieldDefProto]
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., output_data_type_name: _Optional[str] = ..., input_configs: _Optional[_Iterable[_Union[ToolInputDetails, _Mapping]]] = ..., output_configs: _Optional[_Iterable[_Union[ToolOutputDetails, _Mapping]]] = ..., config_fields: _Optional[_Iterable[_Union[_velox_field_def_pb2.VeloxFieldDefProto, _Mapping]]] = ...) -> None: ...

class ToolDetailsResponse(_message.Message):
    __slots__ = ("tool_framework_version", "tool_details")
    TOOL_FRAMEWORK_VERSION_FIELD_NUMBER: _ClassVar[int]
    TOOL_DETAILS_FIELD_NUMBER: _ClassVar[int]
    tool_framework_version: int
    tool_details: _containers.RepeatedCompositeFieldContainer[ToolDetails]
    def __init__(self, tool_framework_version: _Optional[int] = ..., tool_details: _Optional[_Iterable[_Union[ToolDetails, _Mapping]]] = ...) -> None: ...
