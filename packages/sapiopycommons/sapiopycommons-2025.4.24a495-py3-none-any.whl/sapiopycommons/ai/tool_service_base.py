from __future__ import annotations

import json
import traceback
from abc import abstractmethod, ABC
from typing import Any

from grpc import ServicerContext

from sapiopycommons.ai.api.fielddefinitions.proto.velox_field_def_pb2 import VeloxFieldDefProto
from sapiopycommons.general.aliases import FieldMap
from sapiopylib.rest.User import SapioUser

from sapiopycommons.ai.api.plan.tool.proto.entry_pb2 import StepEntryOutputData, StepEntryData, StepJsonData, DataType, \
    StepImageData, StepTextData, StepCsvData, StepBinaryData, StepCsvHeaderRow, StepCsvRow
from sapiopycommons.ai.api.plan.tool.proto.tool_pb2 import ProcessStepRequest, ToolDetailsRequest, ToolDetailsResponse, \
    ProcessStepResponse, ToolDetails, StepRecord, StepRecordFieldValue, ToolInputDetails, ToolOutputDetails
from sapiopycommons.ai.api.plan.tool.proto.tool_pb2_grpc import ToolServiceServicer
from sapiopycommons.ai.api.session.proto.sapio_conn_info_pb2 import SapioConnectionInfo, SapioUserSecretType


class SapioToolResult(ABC):
    """
    A class representing a result from a Sapio tool. Instantiate one of the subclasses to create a result object.
    """

    @abstractmethod
    def to_proto(self) -> StepEntryOutputData | list[StepRecord]:
        """
        Convert this SapioToolResult object to a StepEntryOutputData or list of StepRecord proto objects.
        """
        pass


class BinaryResult(SapioToolResult):
    """
    A class representing binary results from a Sapio tool.
    """
    binary_data: list[bytes]

    def __init__(self, binary_data: list[bytes]):
        """
        :param binary_data: The binary data as a list of bytes. Each entry in the list represents a separate binary
            entry.
        """
        self.binary_data = binary_data

    def to_proto(self) -> StepEntryOutputData | list[StepRecord]:
        return StepEntryOutputData(
            entry_data=StepEntryData(
                dataType=DataType.BINARY,
                binary_data=StepBinaryData(entries=self.binary_data)
            )
        )


class CsvResult(SapioToolResult):
    """
    A class representing CSV results from a Sapio tool.
    """
    csv_data: list[dict[str, Any]]

    def __init__(self, csv_data: list[dict[str, Any]]):
        """
        :param csv_data: The list of CSV data results, provided as a list of dictionaries of column name to value.
            Each entry in the list represents a separate row in the CSV.
        """
        self.csv_data = csv_data

    def to_proto(self) -> StepEntryOutputData | list[StepRecord]:
        return StepEntryOutputData(
            entry_data=StepEntryData(
                dataType=DataType.CSV,
                csv_data=StepCsvData(
                    header=StepCsvHeaderRow(cells=self.csv_data[0].keys()),
                    entries=[StepCsvRow(cells=[str(x) for x in row.values()]) for row in self.csv_data]
                )
            ) if self.csv_data else None
        )


class FieldMapResult(SapioToolResult):
    """
    A class representing field map results from a Sapio tool.
    """
    field_maps: list[FieldMap]

    def __init__(self, field_maps: list[FieldMap]):
        """
        :param field_maps: A list of field maps, where each map is a dictionary of field names to values. Each entry
            will create a new data record in the system.
        """
        self.field_maps = field_maps

    def to_proto(self) -> StepEntryOutputData | list[StepRecord]:
        new_records: list[StepRecord] = []
        for field_map in self.field_maps:
            fields: dict[str, StepRecordFieldValue] = {}
            for field, value in field_map.items():
                field_value = StepRecordFieldValue()
                if isinstance(value, str):
                    field_value.string_value = value
                elif isinstance(value, int):
                    field_value.int_value = value
                elif isinstance(value, float):
                    field_value.double_value = value
                elif isinstance(value, bool):
                    field_value.bool_value = value
                fields[field] = field_value
            new_records.append(StepRecord(fields=fields))
        return new_records


class ImageResult(SapioToolResult):
    """
    A class representing image results from a Sapio tool.
    """
    image_format: str
    image_data: list[bytes]

    def __init__(self, image_format: str, image_data: list[bytes]):
        """
        :param image_format: The format of the image (e.g., PNG, JPEG).
        :param image_data: The image data as a list of bytes. Each entry in the list represents a separate image.
        """
        self.image_format = image_format
        self.image_data = image_data

    def to_proto(self) -> StepEntryOutputData | list[StepRecord]:
        return StepEntryOutputData(
            entry_data=StepEntryData(
                dataType=DataType.IMAGE,
                image_data=StepImageData(
                    image_format=self.image_format,
                    entries=self.image_data)
            )
        )


class JsonResult(SapioToolResult):
    """
    A class representing JSON results from a Sapio tool.
    """
    json_data: list[Any]

    def __init__(self, json_data: list[Any]):
        """
        :param json_data: The list of JSON data results. Each entry in the list represents a separate JSON object.
            These entries must be able to be serialized to JSON using json.dumps(). A common JSON data type is a
            dictionary of strings to strings, integers, doubles, or booleans.
        """
        self.json_data = json_data

    def to_proto(self) -> StepEntryOutputData | list[StepRecord]:
        return StepEntryOutputData(
            entry_data=StepEntryData(
                dataType=DataType.JSON,
                json_data=StepJsonData(entries=[json.dumps(x) for x in self.json_data])
            )
        )


class TextResult(SapioToolResult):
    """
    A class representing text results from a Sapio tool.
    """
    text_data: list[str]

    def __init__(self, text_data: list[str]):
        """
        :param text_data: The text data as a list of strings. Each entry in the list represents a separate text entry.
        """
        self.text_data = text_data

    def to_proto(self) -> StepEntryOutputData | list[StepRecord]:
        return StepEntryOutputData(
            entry_data=StepEntryData(
                dataType=DataType.TEXT,
                text_data=StepTextData(entries=self.text_data)
            )
        )


class ToolServiceBase(ToolServiceServicer, ABC):
    """
    A base class for implementing a tool service. Subclasses should implement the register_tools method to register
    their tools with the service.
    """
    def GetToolDetails(self, request: ToolDetailsRequest, context: ServicerContext) -> ToolDetailsResponse:
        try:
            # Get the tool details from the registered tools.
            details: list[ToolDetails] = self.get_details()
            return ToolDetailsResponse(tool_framework_version=self.tool_version(), tool_details=details)
        except Exception:
            # TODO: This response doesn't even allow logs. What should we do if an exception occurs in this case?
            return ToolDetailsResponse()

    def ProcessData(self, request: ProcessStepRequest, context: ServicerContext) -> ProcessStepResponse:
        try:
            # Convert the SapioConnectionInfo proto object to a SapioUser object.
            user = self.create_user(request.sapio_user)
            # Get the tool results from the registered tool matching the request and convert them to proto objects.
            entry_data: list[StepEntryOutputData] = []
            new_records: list[StepRecord] = []
            # TODO: Make use of the success value after the response object has a field for it.
            success, results, logs = self.run(user, request, context)
            for result in results:
                data: StepEntryOutputData | list[StepRecord] = result.to_proto()
                if isinstance(data, StepEntryOutputData):
                    entry_data.append(data)
                else:
                    new_records.extend(data)
            # Return a ProcessStepResponse proto object containing the output data and new records to the caller.
            return ProcessStepResponse(entry_data=entry_data, log=logs, new_records=new_records)
        except Exception:
            # TODO: Return a False success result after the response object has a field for it.
            return ProcessStepResponse(log=[traceback.format_exc()])

    @staticmethod
    def create_user(info: SapioConnectionInfo, timeout_seconds: int = 60) -> SapioUser:
        """
        Create a SapioUser object from the given SapioConnectionInfo proto object.

        :param info: The SapioConnectionInfo proto object.
        :param timeout_seconds: The request timeout for calls made from this user object.
        """
        # TODO: Have a customizable request timeout? Would need to be added to the request object.
        # TODO: How should the RMI hosts and port be used in the connection info?
        user = SapioUser(info.webservice_url, True, timeout_seconds, guid=info.app_guid)
        if info.secret_type == SapioUserSecretType.SESSION_TOKEN:
            user.api_token = info.secret
        elif info.secret_type == SapioUserSecretType.PASSWORD:
            # TODO: Will the secret be base64 encoded if it's a password? That's how basic auth is normally handled.
            user.password = info.secret
        else:
            raise Exception(f"Unexpected secret type: {info.secret_type}")
        return user

    @staticmethod
    def tool_version() -> int:
        """
        :return: The version of this tool.
        """
        return 1

    def _get_tools(self) -> list[ToolBase]:
        """
        return: Get the tools registered with this service.
        """
        tools: list[ToolBase] = self.register_tools()
        if not tools:
            raise Exception("No tools registered with this service.")
        return tools

    def _get_tool(self, name: str) -> ToolBase:
        """
        Get a specific tool by its name.

        :param name: The name of the tool to retrieve.
        :return: The tool object corresponding to the given name.
        """
        tools: dict[str, ToolBase] = {x.name: x for x in self.register_tools()}
        if not tools:
            raise Exception("No tools registered with this service.")
        if name not in tools:
            raise Exception(f"Tool \"{name}\" not found in registered tools.")
        return tools[name]

    @abstractmethod
    def register_tools(self) -> list[ToolBase]:
        """
        Register the tools with this service. Create and instantiate ToolBase subclasses to register them.

        :return: A list of tools to register to this service.
        """
        pass

    def get_details(self) -> list[ToolDetails]:
        """
        Get the details of the tool.

        :return: A ToolDetailsResponse object containing the tool details.
        """
        tool_details: list[ToolDetails] = []
        for tool in self._get_tools():
            tool_details.append(tool.to_proto())
        return tool_details

    def run(self, user: SapioUser, request: ProcessStepRequest, context: ServicerContext) \
            -> tuple[bool, list[SapioToolResult], list[str]]:
        """
        Execute a tool from this service.

        :param user: A user object that can be used to initialize manager classes using DataMgmtServer to query the
            system.
        :param request: The request object containing the input data.
        :param context: The gRPC context.
        :return: Whether or not the tool succeeded, the results of the tool, and any logs generated by the tool.
        """
        tool = self._get_tool(request.tool_name)
        try:
            results = tool.run(user, request, context)
            return True, results, tool.logs
        except Exception:
            tool.log_message(traceback.format_exc())
            return False, [], tool.logs


class ToolBase(ABC):
    """
    A base class for implementing a tool.
    """
    name: str
    description: str
    data_type_name: str | None
    inputs: list[ToolInputDetails]
    outputs: list[ToolOutputDetails]
    configs: list[VeloxFieldDefProto]
    logs: list[str]

    def __init__(self, name: str, description: str, data_type_name: str | None = None):
        """
        :param name: The name of the tool.
        :param description: A description of the tool.
        :param data_type_name: The name of the output data type of this tool, if applicable. When this tool returns
            FieldMapResult objects in its run method, this name will be used to set the data type of the output data.
        """
        self.name = name
        self.description = description
        self.data_type_name = data_type_name
        self.inputs = []
        self.outputs = []
        self.configs = []
        self.logs = []

    def add_input(self, details: ToolInputDetails) -> None:
        """
        Add an input configuration to the tool. This determines how many inputs this tool will accept in the plan
        manager, as well as what those inputs are.

        :param details: The input configuration details.
        """
        self.inputs.append(details)

    def add_output(self, details: ToolOutputDetails) -> None:
        """
        Add an output configuration to the tool. This determines how many outputs this tool will return in the plan
        manager, as well as what those outputs are.

        :param details: The output configuration details.
        """
        self.outputs.append(details)

    def add_config_field(self, field: VeloxFieldDefProto) -> None:
        """
        Add a configuration field to the tool. This field will be used to configure the tool in the plan manager.

        :param field: The configuration field details.
        """
        self.configs.append(field)

    def to_proto(self) -> ToolDetails:
        """
        :return: The ToolDetails proto object representing this tool.
        """
        return ToolDetails(
            name=self.name,
            description=self.description,
            input_configs=self.inputs,
            output_configs=self.outputs,
            output_data_type_name=self.data_type_name,
            config_fields=self.configs
        )

    def log_message(self, message: str) -> None:
        """
        Log a message for this tool. This message will be included in the logs returned to the caller.

        :param message: The message to log.
        """
        self.logs.append(message)

    @abstractmethod
    def run(self, user: SapioUser, request: ProcessStepRequest, context: ServicerContext) -> list[SapioToolResult]:
        """
        Execute this tool.

        :param user: A user object that can be used to initialize manager classes using DataMgmtServer to query the
            system.
        :param request: The request object containing the input data.
        :param context: The gRPC context.
        :return: A SapioToolResults object containing the response data.
        """
        pass
