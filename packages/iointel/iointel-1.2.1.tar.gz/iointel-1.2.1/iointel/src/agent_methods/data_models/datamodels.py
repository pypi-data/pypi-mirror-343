import sys
from pydantic import BaseModel, Field, ConfigDict, SecretStr

from typing import (
    List,
    Annotated,
    Optional,
    Union,
    Callable,
    Dict,
    Any,
    Literal,
)
from pydantic_ai.models.openai import OpenAIModel
from datetime import datetime

if sys.version_info < (3, 12):
    from typing_extensions import TypedDict
else:
    from typing import TypedDict


from marvin.memory.memory import Memory
from ...utilities.func_metadata import func_metadata, FuncMetadata
from ...utilities.exceptions import ToolError
import inspect


# monkey patching for OpenAIModel to return a generic schema
def patched_get_json_schema(cls, core_schema, handler):
    # Return a generic schema for the OpenAIModel.
    # Adjust this as needed for your application.
    return {"type": "object", "title": cls.__name__}


# Monkey-patch the __get_pydantic_json_schema__ on OpenAIModel.
OpenAIModel.__get_pydantic_json_schema__ = classmethod(patched_get_json_schema)


###### persona ########
class PersonaConfig(BaseModel):
    """
    A configuration object that describes an agent's persona or character.
    """

    name: Optional[str] = Field(
        None, description="If the persona has a specific name or nickname."
    )
    age: Optional[int] = Field(
        None, description="Approximate age of the persona (if relevant).", ge=1
    )
    role: Optional[str] = Field(
        None,
        description="General role or type, e.g. 'a brave knight', 'a friendly teacher', etc.",
    )
    style: Optional[str] = Field(
        None,
        description="A short description of the agent's style or demeanor (e.g., 'formal and polite').",
    )
    domain_knowledge: List[str] = Field(
        default_factory=list,
        description="List of domains or special areas of expertise the agent has.",
    )
    quirks: Optional[str] = Field(
        None,
        description="Any unique quirks or mannerisms, e.g. 'likes using puns' or 'always references coffee.'",
    )
    bio: Optional[str] = Field(
        None, description="A short biography or personal background for the persona."
    )
    lore: Optional[str] = Field(
        None,
        description="In-universe lore or backstory, e.g. 'grew up in a small village with magical powers.'",
    )
    personality: Optional[str] = Field(
        None,
        description="A more direct statement of the persona's emotional or psychological traits.",
    )
    conversation_style: Optional[str] = Field(
        None,
        description="How the character speaks in conversation, e.g., 'often uses slang' or 'very verbose and flowery.'",
    )
    description: Optional[str] = Field(
        None,
        description="A general descriptive text, e.g., 'A tall, lean figure wearing a cloak, with a stern demeanor.'",
    )

    friendliness: Optional[Union[float, str]] = Field(
        None,
        description="How friendly the agent is, from 0 (hostile) to 1 (friendly).",
        ge=0,
        le=1,
    )
    creativity: Optional[Union[float, str]] = Field(
        None,
        description="How creative the agent is, from 0 (very logical) to 1 (very creative).",
        ge=0,
        le=1,
    )
    curiosity: Optional[Union[float, str]] = Field(
        None,
        description="How curious the agent is, from 0 (disinterested) to 1 (very curious).",
        ge=0,
        le=1,
    )
    empathy: Optional[Union[float, str]] = Field(
        None,
        description="How empathetic the agent is, from 0 (cold) to 1 (very empathetic).",
        ge=0,
        le=1,
    )
    humor: Optional[Union[float, str]] = Field(
        None,
        description="How humorous the agent is, from 0 (serious) to 1 (very humorous).",
        ge=0,
        le=1,
    )
    formality: Optional[Union[float, str]] = Field(
        None,
        description="How formal the agent is, from 0 (very casual) to 1 (very formal).",
        ge=0,
        le=1,
    )
    emotional_stability: Optional[Union[float, str]] = Field(
        None,
        description="How emotionally stable the agent is, from 0 (very emotional) to 1 (very stable).",
        ge=0,
        le=1,
    )

    def to_system_instructions(self) -> str:
        """
        Combine fields into a single string that can be appended to the system instructions.
        Each field is optional; only non-empty fields get appended.
        """
        lines = []

        # 1. Possibly greet with a name or reference it
        if self.name:
            lines.append(f"Your name is {self.name}.")

        # 2. Age or approximate range
        if self.age is not None:
            lines.append(f"You are {self.age} years old (approximately).")

        # 3. High-level role or type
        if self.role:
            lines.append(f"You are {self.role}.")

        # 4. Style or demeanor
        if self.style:
            lines.append(f"Your style or demeanor is: {self.style}.")

        # 5. Domain knowledge
        if self.domain_knowledge:
            knowledge_str = ", ".join(self.domain_knowledge)
            lines.append(f"You have expertise or knowledge in: {knowledge_str}.")

        # 6. Quirks
        if self.quirks:
            lines.append(f"You have the following quirks: {self.quirks}.")

        # 7. Bio
        if self.bio:
            lines.append(f"Personal background: {self.bio}.")

        # 8. Lore
        if self.lore:
            lines.append(f"Additional lore/backstory: {self.lore}.")

        # 9. Personality
        if self.personality:
            lines.append(f"Your personality traits: {self.personality}.")

        # 10. Conversation style
        if self.conversation_style:
            lines.append(
                f"In conversation, you speak in this style: {self.conversation_style}."
            )

        # 11. General description
        if self.description:
            lines.append(f"General description: {self.description}.")

        # 12. Personality traits
        if self.friendliness is not None:
            lines.append(
                f"Your overall Friendliness from 0 to 1 is: {self.friendliness}"
            )

        if self.creativity is not None:
            lines.append(f"Your overall Creativity from 0 to 1 is: {self.creativity}")

        if self.curiosity is not None:
            lines.append(f"Your overall Curiosity from 0 to 1 is: {self.curiosity}")

        if self.empathy is not None:
            lines.append(f"Your overall Empathy from 0 to 1 is: {self.empathy}")

        if self.humor is not None:
            lines.append(f"Your overall Humor from 0 to 1 is: {self.humor}")

        if self.formality is not None:
            lines.append(f"Your overall Formality from 0 to 1 is: {self.formality}")

        if self.emotional_stability is not None:
            lines.append(
                f"Your overall Emotional stability from 0 to 1 is: {self.emotional_stability}"
            )

        # Return them joined by newlines, or any separator you prefer
        return "\n".join(lines)


class Tool(BaseModel):
    name: str = Field(description="Name of the tool")
    description: str = Field(description="Description of what the tool does")
    parameters: dict = Field(description="JSON schema for tool parameters")
    is_async: bool = Field(description="Whether the tool is async")
    body: Optional[str] = Field(None, description="Source code of the tool function")
    # fn and fn_metadata are excluded from serialization.
    fn: Optional[Callable] = Field(default=None, exclude=True)
    fn_metadata: Optional[FuncMetadata] = Field(default=None, exclude=True)

    class Config:
        arbitrary_types_allowed = True

    def __call__(self, *args, **kwargs):
        if self.fn:
            return self.fn(*args, **kwargs)
        raise ValueError(f"Tool {self.name} has not been rehydrated correctly.")

    @property
    def __name__(self):
        if self.fn and hasattr(self.fn, "__name__"):
            return self.fn.__name__
        return self.name  # fallback to the Tool's name

    @classmethod
    def from_function(
        cls, fn: Callable, name: Optional[str] = None, description: Optional[str] = None
    ) -> "Tool":
        func_name = name or fn.__name__
        if func_name == "<lambda>":
            raise ValueError("You must provide a name for lambda functions")
        func_doc = description or fn.__doc__ or ""
        is_async = inspect.iscoroutinefunction(fn)
        func_arg_metadata = func_metadata(fn)
        parameters = func_arg_metadata.arg_model.model_json_schema()
        # If fn is already a Tool instance, use its body
        if isinstance(fn, cls) and fn.body:
            body = fn.body
        else:
            try:
                body = inspect.getsource(fn)
            except Exception:
                body = None
        return cls(
            fn=fn,
            name=func_name,
            description=func_doc,
            parameters=parameters,
            fn_metadata=func_arg_metadata,
            is_async=is_async,
            body=body,
        )

    async def run(self, arguments: dict) -> Any:
        """Run the tool with arguments."""
        try:
            return await self.fn_metadata.call_fn_with_arg_validation(
                self.fn, self.is_async, arguments
            )
        except Exception as e:
            raise ToolError(f"Error executing tool {self.name}: {e}") from e


##agent params###
class AgentParams(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        serializers={SecretStr: lambda s: s.get_secret_value()},
    )
    name: Optional[str] = None
    instructions: Optional[str] = None
    description: Optional[str] = None
    swarm_name: Optional[str] = None
    model: Optional[Union[OpenAIModel, str]] = Field(
        default="meta-llama/Llama-3.3-70B-Instruct",
        description="Model or model name for the agent",
    )
    api_key: Optional[Union[str, SecretStr]] = Field(
        None, description="API key for the model, if required."
    )
    base_url: Optional[str] = Field(
        None, description="Base URL for the model, if required."
    )
    tools: Optional[List[Tool]] = Field(default_factory=list)
    memories: Optional[list[Memory]] = Field(default_factory=list)
    model_settings: Optional[Dict[str, Any]] = Field(default_factory=dict)


# reasoning agent
class ReasoningStep(BaseModel):
    explanation: str = Field(
        description="""
            A brief (<5 words) description of what you intend to
            achieve in this step, to display to the user.
            """
    )
    reasoning: str = Field(
        description="A single step of reasoning, not more than 1 or 2 sentences."
    )
    found_validated_solution: bool
    proposed_solution: str = Field(description="The proposed solution for the problem.")


class Swarm(BaseModel):
    members: List[AgentParams]


##summary
class SummaryResult(BaseModel):
    summary: str
    key_points: List[str]


# translation
class TranslationResult(BaseModel):
    translated: str
    target_language: str


Activation = Annotated[float, Field(ge=0, le=1)]


class ModerationException(Exception):
    """Exception raised when a message is not allowed."""

    ...


class ViolationActivation(TypedDict):
    """Violation activation."""

    extreme_profanity: Annotated[Activation, Field(description="hell / damn are fine")]
    sexually_explicit: Activation
    hate_speech: Activation
    harassment: Activation
    self_harm: Activation
    dangerous_content: Activation


##### task and workflow models ########
class BaseStage(BaseModel):
    stage_id: Optional[int] = None
    stage_name: str = ""


class SimpleStage(BaseStage):
    stage_type: Literal["simple"] = "simple"
    objective: str
    result_type: Any = None
    agents: List[Union[AgentParams, Swarm]] = Field(default_factory=list)
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)


class SequentialStage(BaseStage):
    stage_type: Literal["sequential"] = "sequential"
    stages: List["Stage"] = Field(
        ..., description="List of stages to execute sequentially"
    )


class ParallelStage(BaseStage):
    stage_type: Literal["parallel"] = "parallel"
    # merge_strategy: Optional[str] = None
    stages: List["Stage"] = Field(
        ..., description="List of stages to execute in parallel"
    )


class WhileStage(BaseStage):
    stage_type: Literal["while"] = "while"
    condition: str | Callable = Field(
        ...,
        description=(
            "A condition (expressed as a string or expression) that determines whether "
            "the loop should continue. The evaluation of this condition should be handled "
            "by the executor logic."
        ),
    )
    max_iterations: Optional[int] = Field(
        100,
        description="An optional safeguard to limit the number of iterations and prevent infinite loops.",
    )
    stage: List["Stage"] = Field(..., description="The loop body")


class FallbackStage(BaseStage):
    stage_type: Literal["fallback"] = "fallback"
    primary: "Stage" = Field(..., description="The primary stage to execute")
    fallback: "Stage" = Field(
        ..., description="The fallback stage to execute if primary fails"
    )


Stage = Union[SimpleStage, ParallelStage, WhileStage, FallbackStage]


FallbackStage.model_rebuild()
ParallelStage.model_rebuild()
SequentialStage.model_rebuild()
WhileStage.model_rebuild()


class TaskDefinition(BaseModel):
    task_id: str
    name: str
    # description: Optional[str] = None
    text: Optional[str] = None
    agents: Optional[Union[List[AgentParams], Swarm]] = None
    task_metadata: Optional[Dict[str, Any]] = None
    # metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    execution_metadata: Optional[Dict[str, Any]] = None
    # execution_mode: Literal["sequential", "parallel"] = "sequential"
    # stages: List[Stage] = Field(..., description="The sequence of stages that make up this task")


class WorkflowDefinition(BaseModel):
    """
    The top-level structure of the YAML.
    - name: A human-readable name for the workflow
    - agents: The agent definitions
    - tasks: The list of tasks that make up the workflow
    """

    name: str
    text: Optional[str] = None  # Main text/prompt for the workflow
    client_mode: Optional[bool] = None
    agents: Optional[Union[List[AgentParams], Swarm]] = None
    tasks: List[TaskDefinition] = Field(default_factory=list)


### logging handlers


class BaseEventModel(BaseModel):
    """
    A base model to capture common fields or structure for all events.
    """

    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentMessageEvent(BaseEventModel):
    event_type: str = "agent_message"
    agent_name: str
    content: str


class UserMessageEvent(BaseEventModel):
    event_type: str = "user_message"
    content: str


class OrchestratorMessageEvent(BaseEventModel):
    event_type: str = "orchestrator_message"
    content: str


class ToolCallEvent(BaseEventModel):
    event_type: str = "tool_call"
    tool_name: str


class ToolResultEvent(BaseEventModel):
    event_type: str = "tool_result"
    tool_name: str
    result: str


class OrchestratorStartEvent(BaseEventModel):
    event_type: str = "orchestrator_start"


class OrchestratorEndEvent(BaseEventModel):
    event_type: str = "orchestrator_end"


class AgentMessageDeltaEvent(BaseEventModel):
    event_type: str = "agent_message_delta"
    delta: str


class OrchestratorErrorEvent(BaseEventModel):
    event_type: str = "orchestrator_error"
    error: str


class EndTurnEvent(BaseEventModel):
    event_type: str = "end_turn"


class CatchallEvent(BaseEventModel):
    event_type: str = "catch-all"
    details: dict = {}


# Union of all event models
EventModelUnion = Union[
    AgentMessageEvent,
    UserMessageEvent,
    OrchestratorMessageEvent,
    ToolCallEvent,
    ToolResultEvent,
    OrchestratorStartEvent,
    OrchestratorEndEvent,
    AgentMessageDeltaEvent,
    OrchestratorErrorEvent,
    EndTurnEvent,
    CatchallEvent,
]


class EventsLog(BaseModel):
    """
    Main aggregator for all events.
    """

    events: List[EventModelUnion] = []
