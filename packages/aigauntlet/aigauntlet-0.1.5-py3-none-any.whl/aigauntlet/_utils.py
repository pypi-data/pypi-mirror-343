import inspect
from copy import deepcopy
from enum import Enum
from typing import Any, Callable, Type, get_type_hints

import requests
from pydantic import BaseModel

from .url_utils import get_api_endpoint


class SuccessCode(Enum):
    """Concisely describes the type of a probe's result. Part of a ProbeResult object."""

    PLACEHOLDER = -1  # used for ProbeResults that are not yet set.
    ERROR = 0  # there was an error with this probe
    COMPLIANT = (
        1  # the agent did NOT fall for the PROBE, it is compliant with the CAPABILITY
    )
    NONCOMPLIANT = 2  # the agent DID fall for the probe and showed the bad behavior.
    CONTINUE = 3  # used for probes that have multiple steps.


class ProbeResult:
    """The result of a probe. Object returned by Probe::applyTo."""

    def __init__(
        self, success_code: SuccessCode, description: str = "", extra: Any = None
    ):
        self.success_code = success_code
        self.description = description
        self.extra = extra

    def to_dict(self) -> dict:
        """Convert ProbeResult to a JSON-serializable dictionary."""
        return {
            "success_code": self.success_code.name,
            "description": self.description,
            "extra": self.extra,
        }


class TrialReport:
    """The base class for trial reports. Trial reports are
    what are returned when a trial is run."""

    def __init__(self, results: Any):
        self.results = deepcopy(results)
        # NOTE: convert all the success_codes to SuccessCode enum  This will look different for each report based on the contents of the report so implement this in the derived class.

    def get_results(self) -> Any:
        """Returns the results in a dictionary format."""
        # NOTE: override this in the derived class if you want to return a different format.
        return self.results

    def visualize_report(self) -> Any:
        """Visualizes the report."""
        raise NotImplementedError("This method must be implemented in a derived class.")


class TrialInterface:
    """Abstract base class for trial interfaces. A trial interface is how end users interact with a trial."""

    def __init__(
        self,
        email: str,
        api_key: str,
        input_format: Type[BaseModel],
        output_format: Type[BaseModel],
        interact_function: Callable,  # takes input_format, returns output_format
    ):
        self.email = email
        self.api_key = api_key
        self.input_format = input_format
        # the format of the input that the agent will be receiving
        self.output_format = output_format
        # the format of the output that the agent will be returning
        self.interact_function = interact_function
        # the function that the agent will be using to get the input and return the output

        # validate the input and output formats
        if not issubclass(self.input_format, BaseModel):
            raise ValueError("input_format must be a subclass of BaseModel")
        if not issubclass(self.output_format, BaseModel):
            raise ValueError("output_format must be a subclass of BaseModel")
        if not callable(self.interact_function):
            raise ValueError("interact_function must be a callable")

        # Make sure the input function fits the input / output formats.
        hints = get_type_hints(self.interact_function)
        sig = inspect.signature(self.interact_function)
        params = list(sig.parameters.values())

        if not params or len(params) != 1:
            raise ValueError("interact_function must take exactly one argument")

        # accept the exact input format as long as it's included in the union type
        param_type = hints.get(params[0].name)
        if (
            param_type is None
            or not isinstance(param_type, type)
            or not (
                param_type == self.input_format
                or (
                    hasattr(param_type, "__origin__")
                    and hasattr(param_type, "__args__")
                    and self.input_format in param_type.__args__
                )
            )
        ):
            raise ValueError(
                f"interact_function's input type must be {self.input_format} or include it as a union type"
            )

        return_type = hints.get("return")
        if return_type != self.output_format:
            raise ValueError(
                f"interact_function's return type must be {self.output_format}"
            )

        # send a request to make sure the user is valid
        response = requests.post(
            get_api_endpoint("check_user"),
            headers={"Authorization": api_key},
            json={"email": email},
        )
        if response.status_code != 200:
            raise ValueError("User is not valid")
        if response.json()["is_deleted"] is True:
            raise ValueError("User is deleted")
        if response.json()["credit_left"] <= 0:
            raise ValueError("User has no credits left")

    def run(self) -> TrialReport:
        """Runs the trial. Returns a trial report."""
        raise NotImplementedError("This method must be implemented in a derived class.")
