import itertools
from typing import Dict, List, Literal, cast, AsyncGenerator, Sequence
from autogen_agentchat.teams import BaseGroupChat
from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.base import (
    TerminationCondition,
    AndTerminationCondition,
    OrTerminationCondition,
)
from autogen_agentchat.conditions import (
    TextMentionTermination,
)

from autogen_agentchat.base import TaskResult

from ..base.types import Registry, ChatMessage, ReturnMessage, TOTAL_MODELS_NAME
from ..message import return_last_message


def get_termination_conditions(termination_condition: TerminationCondition) -> Sequence[str]:
    if isinstance(termination_condition, str):
        return [termination_condition]

    if isinstance(termination_condition, TextMentionTermination):
        return [termination_condition._termination_text]
    
    if isinstance(termination_condition, OrTerminationCondition) or isinstance(termination_condition, AndTerminationCondition):
        _termination_conditions = [get_termination_conditions(condition) for condition in termination_condition._conditions]
        return list(itertools.chain.from_iterable(_termination_conditions))
    
    return []


class Model:
    def __init__(self):
        self._registry: Dict[str, Registry] = {}

    def _register(
        self,
        name: str,
        actor: BaseGroupChat | BaseChatAgent,
        source_select: str | None = None,
        output_idx: int | None = None,
        termination_conditions: Sequence[str] | None = None,
    ) -> None:
        if isinstance(actor, BaseGroupChat):
            actor_type = "team"
        elif isinstance(actor, BaseChatAgent):
            actor_type = "agent"
        else:
            raise TypeError("actor must be a AutoGen GroupChat(team) or Agent instance")
        
        registry = Registry(
            name=name,
            actor=actor.dump_component(),
            type=actor_type,
            source_select=source_select,
            output_idx=output_idx,
            termination_conditions=termination_conditions or [],
        )
        self._registry[name] = registry

    def register(
        self,
        name: str,
        source_select: str | None = None,
        output_idx: int | None = None,
        actor: BaseGroupChat | BaseChatAgent | None = None,
    ) -> None:
        if name == TOTAL_MODELS_NAME:
            # log, now allowed name
            return
        if source_select is not None and output_idx is not None:
            raise ValueError("source_select and output_idx cannot be used together")
        if source_select is None and output_idx is None:
            output_idx = 0
        if actor is None:
            # If no actor is provided, return a decorator
            def decorator(builder) -> None:
                actor = builder()
                if isinstance(actor, BaseGroupChat):
                    self._register(name, actor, source_select, output_idx, termination_conditions=get_termination_conditions(actor._termination_condition))
                elif isinstance(actor, BaseChatAgent):
                    if output_idx is not None and output_idx != 0:
                        # log warning
                        pass
                    self._register(name, actor, None, output_idx)
                else:
                    print(actor)
                    raise TypeError("actor must be a AutoGen GroupChat(team) or Agent instance")
            return decorator
        else:
            # If an actor is provided, register it directly
            self._register(name, actor, source_select, output_idx, termination_conditions=get_termination_conditions(actor._termination_condition))

    @property
    def model_list(self) -> List[str]:
        """
        Get the list of registered models.

        Returns:
            List[str]: List of model names.
        """
        return list(self._registry.keys())

    # @property
    def _get_actor(self, name) -> BaseGroupChat | BaseChatAgent:
        dump = self._registry[name].actor
        if self._registry[name].type == "team":
            return BaseGroupChat.load_component(dump)
        elif self._registry[name].type == "agent":
            return BaseChatAgent.load_component(dump)
        else:
            raise TypeError("actor must be a AutoGen GroupChat(team) or Agent instance")
        
    async def run_stream(self, name: str, messages: List[ChatMessage]) -> AsyncGenerator[ReturnMessage, None]:
        actor = self._get_actor(name)
        len_messages = len(messages)
        message_count = 0
        if isinstance(actor, BaseGroupChat):
            yield ReturnMessage(content="<think>")

        async for message in actor.run_stream(task=messages):
            if len_messages > message_count:
                message_count += 1
                continue
            if hasattr(message, "content") and message.content:
                yield ReturnMessage(content=f"## [{message.source}]\n\n" + message.to_text())
        else:
            if isinstance(actor, BaseGroupChat):
                yield ReturnMessage(content="</think>")
            # at that point, the message is a TaskResult
            if isinstance(message, TaskResult):
                content, total_prompt_tokens, total_completion_tokens, total_tokens = return_last_message(
                    message,
                    source=self._registry[name].source_select,
                    idx=self._registry[name].output_idx,
                    terminate_texts=self._registry[name].termination_conditions,
                )
                yield ReturnMessage(
                    content=content,
                    total_completion_tokens=total_completion_tokens,
                    total_prompt_tokens=total_prompt_tokens,
                    total_tokens=total_tokens,
                )
            else:
                yield ReturnMessage(
                    content="Somthing went wrong, please try again.",
                    total_completion_tokens=0,
                    total_prompt_tokens=0,
                    total_tokens=0, 
                )
    
    async def run(self, name: str, messages: List[ChatMessage]):
        actor = self._get_actor(name)
        if isinstance(actor, BaseGroupChat):
            async for message in self.run_stream(name, messages):
                continue
            else:
                return message
        elif isinstance(actor, BaseChatAgent):
            messages = await actor.run(task=messages)
            content, total_prompt_tokens, total_completion_tokens, total_tokens = return_last_message(
                messages,
                source=self._registry[name].source_select,
                idx=self._registry[name].output_idx,
                terminate_texts=self._registry[name].termination_conditions,
            )
            return ReturnMessage(
                content=content,
                total_completion_tokens=total_completion_tokens,
                total_prompt_tokens=total_prompt_tokens,
                total_tokens=total_tokens,
            )
        else:
            raise TypeError("actor must be a AutoGen GroupChat(team) or Agent instance")