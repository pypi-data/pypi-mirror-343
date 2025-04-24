import json
from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

from vector_bridge import HTTPException
from vector_bridge.schema.helpers.enums import AIProviders, GPTActions


class FunctionsSorting(str, Enum):
    created_at = "created_at"
    updated_at = "updated_at"


class FunctionPropertyStorageStructure(BaseModel):
    name: str
    description: str
    type: str = Field(default="string")
    items: Dict[str, str] = Field(default_factory=dict)
    enum: List[str] = []
    required: bool = Field(default=False)


class FunctionParametersStorageStructure(BaseModel):
    properties: List[FunctionPropertyStorageStructure]

    def to_dynamodb_raw(self):
        return {
            "properties": {"L": [{"M": _property.to_dynamodb_raw()} for _property in self.properties]},
        }


class Overrides(BaseModel):
    ai_provider: Optional[AIProviders] = Field(default=None)
    model: str = Field(default="")
    system_prompt: str = Field(default="")
    message_prompt: str = Field(default="")
    knowledge_prompt: str = Field(default="")
    max_tokens: str = Field(default="")
    frequency_penalty: str = Field(default="")
    presence_penalty: str = Field(default="")
    temperature: str = Field(default="")


class Function(BaseModel):
    function_id: str
    function_name: str
    integration_id: str
    description: str
    accessible_by_ai: bool = Field(default=True)
    function_parameters: FunctionParametersStorageStructure
    overrides: Overrides = Field(default=Overrides())
    system_required: bool = Field(default=False)
    created_at: str = Field(default="")
    created_by: str = Field(default="")
    updated_at: str = Field(default="")
    updated_by: str = Field(default="")

    @property
    def uuid(self):
        return self.function_id

    @classmethod
    def to_valid_subclass(
        cls, data: dict
    ) -> Union[
        None,
        "OtherFunction",
        "CodeExecuteFunction",
        "SummaryFunction",
        "SemanticSearchFunction",
        "SimilarSearchFunction",
        "JsonFunction",
        "ForwardToAgentFunction",
    ]:
        function_action = data["function_action"]
        if function_action == GPTActions.SEARCH:
            return SemanticSearchFunction.model_validate(data)
        elif function_action == GPTActions.SIMILAR:
            return SimilarSearchFunction.model_validate(data)
        elif function_action == GPTActions.SUMMARY:
            return SummaryFunction.model_validate(data)
        elif function_action == GPTActions.JSON:
            return JsonFunction.model_validate(data)
        elif function_action == GPTActions.CODE_EXEC:
            return CodeExecuteFunction.model_validate(data)
        elif function_action == GPTActions.FORWARD_TO_AGENT:
            return ForwardToAgentFunction.model_validate(data)
        elif function_action == GPTActions.OTHER:
            return OtherFunction.model_validate(data)


class SemanticSearchFunction(Function):
    function_action: GPTActions = GPTActions.SEARCH
    vector_schema: str


class SimilarSearchFunction(Function):
    function_action: GPTActions = GPTActions.SIMILAR
    vector_schema: str


class SummaryFunction(Function):
    function_action: GPTActions = GPTActions.SUMMARY


class JsonFunction(Function):
    function_action: GPTActions = GPTActions.JSON


class CodeExecuteFunction(Function):
    function_action: GPTActions = GPTActions.CODE_EXEC
    code: str


class ForwardToAgentFunction(Function):
    function_action: GPTActions = GPTActions.FORWARD_TO_AGENT


class OtherFunction(Function):
    function_action: GPTActions = GPTActions.OTHER


class FunctionCreate(BaseModel):
    function_name: str
    description: str
    accessible_by_ai: bool = Field(default=True)
    function_parameters: FunctionParametersStorageStructure
    overrides: Overrides = Field(default=Overrides())


class SemanticSearchFunctionCreate(FunctionCreate):
    function_action: GPTActions = GPTActions.SEARCH
    vector_schema: str


class SimilarSearchFunctionCreate(FunctionCreate):
    function_action: GPTActions = GPTActions.SIMILAR
    vector_schema: str


class SummaryFunctionCreate(FunctionCreate):
    function_action: GPTActions = GPTActions.SUMMARY


class JsonFunctionCreate(FunctionCreate):
    function_action: GPTActions = GPTActions.JSON


class CodeExecuteFunctionCreate(FunctionCreate):
    function_action: GPTActions = GPTActions.CODE_EXEC
    code: str


class FunctionUpdate(BaseModel):
    description: str
    accessible_by_ai: bool = Field(default=True)
    function_parameters: FunctionParametersStorageStructure
    overrides: Overrides = Field(default=Overrides())


class SemanticSearchFunctionUpdate(FunctionUpdate):
    function_action: GPTActions = GPTActions.SEARCH
    vector_schema: str


class SimilarSearchFunctionUpdate(FunctionUpdate):
    function_action: GPTActions = GPTActions.SIMILAR
    vector_schema: str


class SummaryFunctionUpdate(FunctionUpdate):
    function_action: GPTActions = GPTActions.SUMMARY


class JsonFunctionUpdate(FunctionUpdate):
    function_action: GPTActions = GPTActions.JSON


class CodeExecuteFunctionUpdate(FunctionUpdate):
    function_action: GPTActions = GPTActions.CODE_EXEC
    code: str


class PaginatedFunctions(BaseModel):
    functions: List[
        Union[
            SemanticSearchFunction,
            SimilarSearchFunction,
            SummaryFunction,
            JsonFunction,
            CodeExecuteFunction,
            ForwardToAgentFunction,
            OtherFunction,
        ]
    ] = Field(default_factory=list)
    limit: int
    last_evaluated_key: Optional[str] = None
    has_more: bool = False

    @classmethod
    def resolve_functions(cls, data: dict) -> "PaginatedFunctions":
        functions = [Function.to_valid_subclass(func) for func in data["functions"]]
        data["functions"] = functions
        return PaginatedFunctions(**data)


class StreamingResponse:
    """
    Processes a binary stream, filtering out <ignore> messages and
    capturing everything inside <response>...</response>. If an <error>...</error>
    message is found, it returns the error instead.
    """

    def __init__(self, stream):
        """
        Initializes the processor with a binary stream (generator).
        :param stream: An iterable or generator that yields binary messages.
        """
        self.stream = stream
        self.buffer = bytearray()
        self.response_content = bytearray()
        self.in_response_block = False

    def response(self) -> Union[str, None]:
        """
        Processes the stream, returning the full data inside <response>...</response>.
        If an <error>...</error> message is found, it returns the error instead.
        """

        def try_parse_json(data):
            decoded_content = data.decode("utf-8").rstrip("\n")
            try:
                return json.loads(decoded_content)
            except (json.JSONDecodeError, TypeError):
                return decoded_content

        for chunk in self.stream:
            if not isinstance(chunk, bytes):
                continue

            # Add the new chunk to our buffer
            self.buffer.extend(chunk)

            # Process ignore tags
            while b"<ignore>\n" in self.buffer:
                ignore_pos = self.buffer.find(b"<ignore>\n")
                self.buffer = self.buffer[:ignore_pos] + self.buffer[ignore_pos + 9 :]

            # Check for error messages
            while b"<error>" in self.buffer and b"</error>" in self.buffer:
                start = self.buffer.find(b"<error>") + 7
                end = self.buffer.find(b"</error>")
                if start <= end:  # Ensure valid positions
                    error_msg = self.buffer[start:end].decode("utf-8").strip()
                    raise HTTPException(status_code=400, detail=error_msg)
                else:
                    # Malformed error tag, remove start tag to avoid infinite loop
                    self.buffer = self.buffer[start:]

                    # Process response blocks
            self._process_response_blocks()

            # If we've found a complete response, return it
            if self.response_content and not self.in_response_block:
                return try_parse_json(self.response_content)

        # Handle case where stream ends inside a response block
        if self.in_response_block and self.response_content:
            return try_parse_json(self.response_content)

        return None

    def _process_response_blocks(self):
        """Helper method to process response blocks in the buffer"""
        # Look for complete inline responses first
        while True:
            start = self.buffer.find(b"<response>")
            end = self.buffer.find(b"</response>")

            if start != -1 and end != -1 and start < end:
                # Complete response found
                content_start = start + 10  # Length of "<response>"

                # Handle the optional newline after opening tag
                if self.buffer[content_start : content_start + 1] == b"\n":
                    content_start += 1

                content = self.buffer[content_start:end]
                self.response_content = content

                # Remove processed part from buffer
                self.buffer = self.buffer[end + 11 :]  # 11 is length of "</response>"
                self.in_response_block = False
                return
            else:
                break

        # Handle start/end tags separately if we didn't find complete response
        if not self.in_response_block and b"<response>" in self.buffer:
            start = self.buffer.find(b"<response>")
            self.in_response_block = True
            content_start = start + 10

            # Handle the optional newline after opening tag
            if len(self.buffer) > content_start and self.buffer[content_start : content_start + 1] == b"\n":
                content_start += 1

            self.response_content = bytearray()
            self.buffer = self.buffer[content_start:]

        if self.in_response_block and b"</response>" in self.buffer:
            end = self.buffer.find(b"</response>")
            content = self.buffer[:end]
            self.response_content.extend(content)
            self.in_response_block = False
            self.buffer = self.buffer[end + 11 :]  # 11 is length of "</response>"

        # If we're in a response block, accumulate content
        if self.in_response_block:
            self.response_content.extend(self.buffer)
            self.buffer = bytearray()
