import functools
import warnings
from textwrap import dedent
from typing import Any, List

from pydantic import BaseModel
from typing_extensions import Self

from autogen_core import Component, ComponentModel
# from autogen_core._function_utils import (
#     get_typed_signature,
# )
from autogen_core.code_executor import Import, ImportFromModule
from autogen_core.code_executor._func_with_reqs import import_to_str, to_code
from autogen_core.models import LLMMessage
from ..base import BaseModifier, BaseModifierAgent
from ..base.types import ModifierFunction
from ..base._base_modifier import BaseModifierFunction


class ModifierConfig(BaseModel):
    """Configuration for a modifier function."""

    source_code: str | None = None
    function: ComponentModel | None = None
    agent: ComponentModel | None = None
    name: str
    global_imports: List[Import]


class Modifier(BaseModifier, Component[ModifierConfig]):
    component_provider_override = "autogen_contextplus.modifier.Modifier"
    component_config_schema = ModifierConfig

    def __init__(
        self,
        func: ModifierFunction | BaseModifierFunction | None = None,
        agent: BaseModifierAgent | None = None,
        name: str | None = None,
        global_imports: List[Import] = [],
        strict: bool = False,
    ) -> None:
        self._func = func
        self._agent = agent
        self._global_imports = global_imports
        self._global_imports.append(
            ImportFromModule(
                module="typing",
                imports=("List", "Optional", "Callable", "Any", "Sequence"),
            )
        )
        self._global_imports.append(
            ImportFromModule(
                module="autogen_core.models",
                imports=("LLMMessage",),
            )
        )
        func_name = ""
        if func is not None:
            func_name = name or func.func.__name__ if isinstance(func, functools.partial) else name or func.__name__
        if agent is not None:
            if not isinstance(agent, BaseModifierAgent):
                raise TypeError(f"Expected a BaseChatAgent but got {type(agent)}")
            func_name = name or agent.name
        if func is None and agent is None:
            raise ValueError("Either a function or an agent must be provided.")
        if func is not None and agent is not None:
            raise ValueError("Only one of a function or an agent can be provided.")
        super().__init__(name=func_name)

    async def run(self, messages: List[LLMMessage], non_modified_messages: List[LLMMessage]) -> List[LLMMessage]:
        if self._func is not None:
            result = self._func(messages, non_modified_messages)
        elif self._agent is not None:
            result = await self._agent.run(task=messages, original_task=non_modified_messages)
        else:
            result = messages
        return result

    def _to_config(self) -> ModifierConfig:
        if self._func is not None and self._agent is not None:
            raise ValueError("Only one of a function or an agent can be provided.")
        elif self._func is not None:
            if not isinstance(self._func, BaseModifierFunction):
                return ModifierConfig(
                    source_code=dedent(to_code(self._func)),
                    global_imports=self._global_imports,
                    name=self.name,
                )
            else:
                return ModifierConfig(
                    function=self._func.dump_component(),
                    global_imports=self._global_imports,
                    name=self.name,
                )
        elif self._agent is not None:
            return ModifierConfig(
                agent=self._agent.dump_component(),
                global_imports=self._global_imports,
                name=self.name,
            )
        else:
            raise ValueError("Either a function or an agent must be provided.")

    @classmethod
    def _from_config(cls, config: ModifierConfig) -> Self:
        if config.source_code is not None and config.function is not None:
            raise ValueError("Only one of a function or an agent can be provided.")
        elif config.source_code is not None and config.agent is not None:
            raise ValueError("Only one of a function or an agent can be provided.")
        elif config.function is not None and config.agent is not None:
            raise ValueError("Only one of a function or an agent can be provided.")

        exec_globals: dict[str, Any] = {}

        # Execute imports first
        for import_stmt in config.global_imports:
            import_code = import_to_str(import_stmt)
            try:
                exec(import_code, exec_globals)
            except ModuleNotFoundError as e:
                raise ModuleNotFoundError(
                    f"Failed to import {import_code}: Module not found. Please ensure the module is installed."
                ) from e
            except ImportError as e:
                raise ImportError(f"Failed to import {import_code}: {str(e)}") from e
            except Exception as e:
                raise RuntimeError(f"Unexpected error while importing {import_code}: {str(e)}") from e
            
        if config.source_code is not None:
            warnings.warn(
                "\n⚠️  SECURITY WARNING ⚠️\n"
                "Loading a FunctionTool from config will execute code to import the provided global imports and and function code.\n"
                "Only load configs from TRUSTED sources to prevent arbitrary code execution.",
                UserWarning,
                stacklevel=2,
            )

            # Execute function code
            try:
                exec(config.source_code, exec_globals)
                func_name = config.source_code.split("def ")[1].split("(")[0]
            except Exception as e:
                raise ValueError(f"Could not compile and load function: {e}") from e

            # Get function and verify it's callable
            func: ModifierFunction = exec_globals[func_name]
            if not callable(func):
                raise TypeError(f"Expected function but got {type(func)}")

            return cls(func=func, name=config.name, global_imports=config.global_imports)
        elif config.agent is not None:
            return cls(agent=BaseModifierAgent.load_component(config.agent), name=config.name, global_imports=config.global_imports)
        elif config.function is not None:
            return cls(func=BaseModifierFunction.load_component(config.function), name=config.name, global_imports=config.global_imports)
        raise ValueError("Either a function or an agent must be provided.")
