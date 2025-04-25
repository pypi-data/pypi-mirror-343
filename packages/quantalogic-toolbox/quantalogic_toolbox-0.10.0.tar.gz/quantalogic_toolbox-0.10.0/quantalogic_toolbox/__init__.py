"""Toolbox package for Quantalogic CodeAct framework."""
from typing import Callable

from .tool import Tool, ToolArgument


def create_tool(func: Callable) -> Tool:
    """Create a Tool instance from a function, preserving confirmation attributes."""
    import inspect

    # Parse function signature to extract arguments
    sig = inspect.signature(func)
    arguments = []
    for param_name, param in sig.parameters.items():
        param_type = param.annotation if param.annotation != param.empty else str
        arguments.append(ToolArgument(
            name=param_name,
            arg_type=str(param_type.__name__) if hasattr(param_type, '__name__') else str(param_type),
            description="",
            required=param.default == param.empty
        ))
    
    # Determine return type
    return_type = sig.return_annotation
    return_type_str = str(return_type.__name__) if hasattr(return_type, '__name__') else str(return_type) if return_type != inspect.Parameter.empty else "None"

    # Create tool instance
    tool = Tool(
        name=func.__name__,
        description=func.__doc__ or "No description provided",
        arguments=arguments,
        return_type=return_type_str
    )
    
    # Set confirmation attributes from function
    tool.requires_confirmation = getattr(func, 'requires_confirmation', False)
    tool.confirmation_message = getattr(func, 'confirmation_message', None)
    
    # Bind the execution function
    if inspect.iscoroutinefunction(func):
        tool.async_execute = func
    else:
        async def async_execute(**kwargs):
            return func(**kwargs)
        tool.async_execute = async_execute
    
    return tool


__all__ = ["Tool", "ToolArgument", "create_tool"]