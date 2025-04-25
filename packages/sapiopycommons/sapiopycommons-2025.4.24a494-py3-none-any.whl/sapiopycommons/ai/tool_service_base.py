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
    A base class for implementing a tool service.

    Subclasses must implement the get_details and run methods to provide specific functionality for the tool.
    """
    tools: list[ToolBase]

    def GetToolDetails(self, request: ToolDetailsRequest, context: ServicerContext) -> ToolDetailsResponse:
        try:
            # Convert the SapioConnectionInfo proto object to a SapioUser object.
            user = self.create_user(request.sapio_conn_info)
            # Get the tool details from the subclass.
            # TODO: Return something other than the ToolDetails proto objects? Something that's cleaner for the
            #  implementing class to work with?
            details: list[ToolDetails] = self.get_details(user, request, context)
            return ToolDetailsResponse(tool_framework_version=self.tool_version(), tool_details=details)
        except Exception as e:
            # TODO: This response doesn't even allow logs. What should we do if an exception occurs in this case?
            return ToolDetailsResponse()

    def ProcessData(self, request: ProcessStepRequest, context: ServicerContext) -> ProcessStepResponse:
        try:
            # Convert the SapioConnectionInfo proto object to a SapioUser object.
            user = self.create_user(request.sapio_user)
            # Get the tool results from the subclass and convert them to proto objects.
            entry_data: list[StepEntryOutputData] = []
            new_records: list[StepRecord] = []
            for result in self.run(user, request, context):
                data: StepEntryOutputData | list[StepRecord] = result.to_proto()
                if isinstance(data, StepEntryOutputData):
                    entry_data.append(data)
                else:
                    new_records.extend(data)
            # Return a ProcessStepResponse proto object containing the output data and new records to the caller.
            # TODO: Return an is_success = true value.
            # TODO: Allow logging in the tools?
            return ProcessStepResponse(entry_data=entry_data, new_records=new_records)
        except Exception as e:
            # TODO: Do something other than dump the full stack trace into the logs?
            # TODO: Eventually we'll return an is_success = false value.
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
        Get the tools registered with this service.
        """
        # If the tools have not been registered, call the register_tools method to do so.
        if not hasattr(self, "tools"):
            self.tools = self.register_tools()
        # If the tools are still not registered, raise an exception.
        if not self.tools:
            raise Exception("No tools registered with this service.")
        return self.tools

    @abstractmethod
    def register_tools(self) -> list[ToolBase]:
        """
        Register the tools with this service.
        """
        pass

    @abstractmethod
    def get_details(self, user: SapioUser, request: ToolDetailsRequest, context: ServicerContext) -> list[ToolDetails]:
        """
        Get the details of the tool.

        :param user: A user object that can be used to initialize manager classes using DataMgmtServer to query the
            system.
        :param request: The request object containing the input data.
        :param context: The gRPC context.
        :return: A ToolDetailsResponse object containing the tool details.
        """
        tool_details: list[ToolDetails] = []
        for tool in self._get_tools():
            tool_details.append(tool.to_proto())
        return tool_details

    @abstractmethod
    def run(self, user: SapioUser, request: ProcessStepRequest, context: ServicerContext) -> list[SapioToolResult]:
        """
        Execute a tool from this service.

        :param user: A user object that can be used to initialize manager classes using DataMgmtServer to query the
            system.
        :param request: The request object containing the input data.
        :param context: The gRPC context.
        :return: A SapioToolResults object containing the response data.
        """
        for tool in self._get_tools():
            if request.tool_name == tool.name:
                return tool.run(user, request, context)
        raise Exception(f"Tool {request.tool_name} not found in registered tools.")


class ToolBase(ABC):
    name: str
    description: str
    data_type_name: str | None
    inputs: list[ToolInputDetails]
    outputs: list[ToolOutputDetails]
    configs: list[VeloxFieldDefProto]

    def __init__(self, name: str, description: str, data_type_name: str | None = None):
        self.name = name
        self.description = description
        self.data_type_name = data_type_name
        self.inputs = []
        self.outputs = []

    def add_input(self, details: ToolInputDetails) -> None:
        """
        Add an input configuration to the tool.

        :param details: The input configuration details.
        """
        self.inputs.append(details)

    def add_output(self, details: ToolOutputDetails) -> None:
        """
        Add an output configuration to the tool.

        :param details: The output configuration details.
        """
        self.outputs.append(details)

    def add_config_field(self, field: VeloxFieldDefProto) -> None:
        """
        Add a configuration field to the tool.

        :param field: The configuration field details.
        """
        self.configs.append(field)

    def to_proto(self) -> ToolDetails:
        """
        Convert this tool to a ToolDetails proto object.

        :return: The ToolDetails proto object.
        """
        return ToolDetails(
            name=self.name,
            description=self.description,
            input_configs=self.inputs,
            output_configs=self.outputs,
            output_data_type_name=self.data_type_name,
            config_fields=self.configs
        )

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
