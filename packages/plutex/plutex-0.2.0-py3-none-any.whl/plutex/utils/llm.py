"""Helper functions for LLM"""

import json
from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    Type,
    TypeVar,
    Union,
)  # Import Callable

from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.runnables import Runnable
from pydantic import BaseModel

from plutex.llm.models import (
    ChatModelType,
    ModelProvider,
    get_model,
    get_model_info,
)  # Import ModelProvider
from plutex.utils.progress import progress

T = TypeVar("T", bound=BaseModel)


def call_llm(
    prompt: Any,
    model_name: str,
    model_provider: str,  # Keep as str for input flexibility
    pydantic_model: Type[T],
    agent_name: Optional[str] = None,
    max_retries: int = 3,
    default_factory=None,
) -> T:
    """
    Makes an LLM call with retry logic, handling both Deepseek and non-Deepseek models.

    Args:
        prompt: The prompt to send to the LLM
        model_name: Name of the model to use
        model_provider: Provider of the model
        pydantic_model: The Pydantic model class to structure the output
        agent_name: Optional name of the agent for progress updates
        max_retries: Maximum number of retries (default: 3)
        default_factory: Optional factory function to create default response on failure

    Returns:
        An instance of the specified Pydantic model, or a default instance on failure.
    """
    # --- Model Initialization and Validation ---
    try:
        # Cast string provider to Enum
        provider_enum = ModelProvider(model_provider)
    except ValueError:
        print(f"Error: Invalid model provider '{model_provider}'")
        return create_default_response(pydantic_model, default_factory)

    model_info = get_model_info(model_name)
    llm: ChatModelType = get_model(model_name, provider_enum)

    if llm is None:
        print(
            f"Error: Could not initialize model '{model_name}' from provider '{model_provider}'"
        )
        return create_default_response(pydantic_model, default_factory)

    # --- Prepare LLM Runnable (Structured Output or Standard) ---
    llm_runnable: Union[Runnable, ChatModelType] = (
        llm  # Keep original llm type for invoke check
    )
    use_json_extraction = False
    if model_info and not model_info.has_json_mode():
        # Model doesn't support JSON mode, will need manual extraction
        use_json_extraction = True
    else:
        # Model supports JSON mode (or we assume it does if model_info is None)
        # Ensure llm is not None before calling methods
        llm_runnable = llm.with_structured_output(
            pydantic_model,
            method="json_mode",
        )

    # --- LLM Call with Retries ---
    for attempt in range(max_retries):
        try:
            # Ensure llm_runnable is not None (shouldn't happen based on checks above, but good practice)
            if llm_runnable is None:
                raise ValueError("LLM runnable became None unexpectedly.")

            # Call the LLM
            result: Union[T, BaseMessage] = llm_runnable.invoke(
                prompt
            )  # Type hint for clarity

            # --- Result Processing ---
            if use_json_extraction:
                # Manual JSON extraction needed (e.g., for Deepseek)
                if isinstance(result, AIMessage) and isinstance(result.content, str):
                    parsed_result = extract_json_from_deepseek_response(result.content)
                    if parsed_result:
                        # Validate and return the Pydantic model
                        return pydantic_model(**parsed_result)
                    else:
                        # Extraction failed, raise error to trigger retry or default
                        raise ValueError(
                            "Failed to extract JSON from response content."
                        )
                else:
                    # Unexpected response format, raise error
                    raise TypeError(
                        f"Expected AIMessage with string content for JSON extraction, got {type(result)}"
                    )
            else:
                # Structured output should already be the correct Pydantic model type T
                if isinstance(result, pydantic_model):
                    return result
                else:
                    # If it's not the expected model, something went wrong
                    raise TypeError(
                        f"Expected Pydantic model {pydantic_model.__name__}, but got {type(result)}"
                    )

        except Exception as e:
            if agent_name:
                progress.update_status(
                    agent_name, None, f"Error - retry {attempt + 1}/{max_retries}"
                )

            if attempt == max_retries - 1:
                print(
                    f"Error in LLM call after {max_retries} attempts for {agent_name or 'unknown agent'}: {e}"
                )
                # On final retry failure, return default
                return create_default_response(pydantic_model, default_factory)

    # Fallback if loop finishes unexpectedly (should not happen)
    print("Error: LLM call loop completed without success or error handling.")
    return create_default_response(pydantic_model, default_factory)


def create_default_response(
    model_class: Type[T], default_factory: Optional[Callable[[], T]] = None
) -> T:  # Use Callable
    """Creates a safe default response, using factory if provided."""
    if default_factory:
        try:
            return default_factory()
        except Exception as e:
            print(f"Error calling default_factory: {e}. Falling back to basic default.")

    # Basic default creation logic (improved)
    default_values: Dict[str, Any] = {}  # Add type hint
    for field_name, field in model_class.model_fields.items():
        # Use field.annotation which holds the type hint
        field_type = field.annotation
        origin = getattr(field_type, "__origin__", None)
        args = getattr(field_type, "__args__", [])

        # Handle Optional types
        is_optional = origin is Union and type(None) in args
        if is_optional:
            # Get the non-None type from Optional[X]
            non_none_type = next((t for t in args if t is not type(None)), None)
            if non_none_type:
                field_type = non_none_type
                origin = getattr(
                    field_type, "__origin__", None
                )  # Re-check origin for nested types like Optional[List[str]]
            else:  # Should not happen for valid Optional
                # If it's Optional, the default should be None
                default_values[field_name] = None
                continue  # Skip further checks for Optional

        # Assign defaults based on the non-Optional type
        if field_type is str:
            default_values[field_name] = "Error: Default value"
        elif field_type is float:
            default_values[field_name] = 0.0
        elif field_type is int:
            default_values[field_name] = 0
        elif origin is dict or field_type is dict:
            default_values[field_name] = {}
        elif origin is list or field_type is list:
            default_values[field_name] = []
        elif origin is Union:  # Handle non-Optional Unions (like Literal)
            # Try using the first argument of the Union/Literal as default
            if args:
                # Ensure the default matches one of the literal types if possible
                # This part might need refinement based on specific Literal types used
                default_values[field_name] = args[0]
            else:
                # Fallback for complex/empty Unions - None might be invalid if not Optional
                # Attempting a more robust fallback might involve checking field.default
                default_values[field_name] = getattr(field, "default", None)
        else:
            # Fallback for other types - None might be invalid if not Optional
            default_values[field_name] = getattr(field, "default", None)

    try:
        return model_class(**default_values)
    except Exception as e:
        print(f"Error creating default Pydantic model instance: {e}")
        # As a last resort, try creating an empty model instance if possible
        try:
            return model_class()
        except Exception:
            # This is highly unlikely if the model is well-defined
            raise TypeError(
                f"Could not create even a basic default for {model_class.__name__}"
            )


def extract_json_from_deepseek_response(content: str) -> Optional[dict]:
    """Extracts JSON from Deepseek's markdown-formatted response."""
    try:
        json_start = content.find("```json")
        if json_start != -1:
            json_text = content[json_start + 7 :]  # Skip past ```json
            json_end = json_text.find("```")
            if json_end != -1:
                json_text = json_text[:json_end].strip()
                return json.loads(json_text)
    except Exception as e:
        print(f"Error extracting JSON from Deepseek response: {e}")
    return None
