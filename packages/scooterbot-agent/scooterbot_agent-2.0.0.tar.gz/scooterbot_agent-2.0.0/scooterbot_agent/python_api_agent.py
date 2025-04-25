from abc import ABC
from abc import abstractmethod
import datetime
import inspect
import textwrap
from agents import Agent as OpenAIAgent
from agents import Runner
from pydantic import BaseModel
from tenacity import retry
from tenacity import stop_after_attempt
from typing import get_type_hints
from typing import Union


from .private_agent import PrivateAgent


class FinalAnswer(BaseModel, ABC):
    pass


class FinalTextAnswer(FinalAnswer):
    answer: str


class APIExecutionPlan(BaseModel):
    pass


class PythonAPIAgent(PrivateAgent, ABC):
    """Base class for agents that interact with python APIs."""

    execution_plan_cls: type[APIExecutionPlan]
    final_answer_cls: type[FinalAnswer]
    model: str

    def __init__(
        self,
        user_id: str,
        execution_plan_cls: type[APIExecutionPlan],
        final_answer_cls: type[FinalAnswer] = FinalTextAnswer,
        model: str = 'gpt-4.1',
    ) -> None:
        super().__init__(user_id=user_id)
        self.execution_plan_cls = execution_plan_cls
        self.final_answer_cls = final_answer_cls
        self.model = model

    async def reply(self, message: str) -> FinalAnswer:
        return await self.answer_with_api(message)

    @abstractmethod
    def overview(cls) -> str:
        """Succinct description of what this API does. To be read by LLM to decide whether to use
        this API."""

    @abstractmethod
    def usage_guide(self) -> str:
        """Detailed description of the API's capabilities and how to invoke them. Should instruct
        the LLM to call the `invoke_api` tool"""

    @abstractmethod
    def invoke_api(self, execution_plan: APIExecutionPlan) -> str:
        """Implements the `invoke_api` tool."""

    @classmethod
    def format_prior_state(cls, state: str) -> str:
        return textwrap.dedent(
            """\
            ====== STATE AS OF {datetime} ======
            {state}
            """
        ).format(
            datetime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            state=state,
        )

    def initial_state(self) -> str:
        return ''

    @retry(stop=stop_after_attempt(3))
    async def answer_with_api(
        self,
        request: str,
        prior_states: str | None = None,
        depth: int = 0,
        max_depth: int = 3
    ) -> str:
        if not prior_states:
            prior_states = self.format_prior_state(self.initial_state())

        planner = OpenAIAgent(
            name='PythonAPIAgent',
            model=self.model,
            instructions=textwrap.dedent(
                '''\
                # Instructions

                You are given `request` and `prior_states`.

                1. As soon as `prior_states` is sufficient to answer request, return a `{final_answer_cls}` object
                2. Else, return an `{execution_plan_cls}` object, so the process can be repeated with the additional data

                # API Usage Guide

                {usage_guide}
                '''
            ).format(
                final_answer_cls=self.final_answer_cls.__name__,
                execution_plan_cls=self.execution_plan_cls.__name__,
                usage_guide=self.usage_guide()
            ),
            output_type=Union[self.execution_plan_cls, self.final_answer_cls],
        )

        result = await Runner().run(
            planner,
            textwrap.dedent(
                '''\
                # Request

                {request}

                # Prior States

                {prior_states}
                '''
            ).format(
                request=request,
                prior_states=prior_states,
            ),
        )

        if isinstance(result.final_output, FinalAnswer):
            return result.final_output.answer
        elif isinstance(result.final_output, APIExecutionPlan):
            self.invoke_api(result.final_output)
            return result.final_output.answer

        if isinstance(result.final_output, self.final_answer_cls):
            return result.final_output.answer
        if isinstance(result.final_output, self.execution_plan_cls):
            new_state = self.invoke_api(result.final_output)
            prior_states += '\n\n' + self.format_prior_state(new_state)
            if depth < max_depth:
                return await self.answer_with_api(request, prior_states, depth + 1, max_depth)
            else:
                return "Sorry, I ran out of steps"


def generate_python_api_doc(cls: type, whitelisted_members: list[str] | None = None) -> str:
    lines = [f'class {cls.__name__}:']

    class_doc = inspect.getdoc(cls)
    if class_doc:
        lines.append(f'    """{class_doc}"""\n')

    annotations = get_type_hints(cls, localns=cls.__dict__)  # type: ignore

    def get_type_name(annotation):
        """Helper function to extract only the class name from a type hint."""
        if annotation is None or annotation is inspect.Signature.empty:
            return "None"
        if isinstance(annotation, type):
            return annotation.__name__
        if hasattr(annotation, "__origin__"):  # Handles generics like `list[Vehicle]`
            origin = annotation.__origin__.__name__
            args = ", ".join(get_type_name(arg) for arg in annotation.__args__)
            return f"{origin}[{args}]"
        return str(annotation)

    if not whitelisted_members:
        whitelisted_members = list(annotations.keys()) + [
            name for name, _ in inspect.getmembers(cls) if not name.startswith("_")
        ]

    for name in whitelisted_members:
        if hasattr(cls, name):
            attr = getattr(cls, name)
            if inspect.isfunction(attr) or inspect.ismethod(attr):  # If it's a function/method
                sig = inspect.signature(attr)
                params = [
                    f"{param.name}: {get_type_name(param.annotation)}"
                    if param.annotation is not inspect.Parameter.empty
                    else param.name
                    for param in sig.parameters.values()
                ]
                return_type = f" -> {get_type_name(sig.return_annotation)}"
                line = f'    def {name}({", ".join(params)}){return_type}'
            else:  # If it's a variable
                line = f'    {name}: {type(attr).__name__}'
            lines.append(line)
        elif name in annotations:
            lines.append(f'    {name}: {get_type_name(annotations[name])}')

    return "\n".join(lines)
