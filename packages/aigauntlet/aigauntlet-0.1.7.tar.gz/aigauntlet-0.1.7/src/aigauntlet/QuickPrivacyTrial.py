from typing import Callable, Optional

import plotly.graph_objects as go  # type: ignore
import requests
from plotly.subplots import make_subplots  # type: ignore
from pydantic import BaseModel, Field

from ._utils import ProbeResult, SuccessCode, TrialInterface, TrialReport
from .registry import TrialRegistry
from .url_utils import get_api_endpoint, get_report_url


class QuickPrivacyTrial_InputFormat(BaseModel):
    prompt: str = Field(
        ...,
        title="Prompt",
        description="The prompt provided by the server that requires the agent's response.",
    )


class QuickPrivacyTrial_OutputFormat(BaseModel):
    client_response: str = Field(
        ..., title="Client Response", description="The response provided by the agent."
    )


class QuickPrivacyTrialReport(TrialReport):
    def __init__(self, results: dict):
        super().__init__(results)  # NOTE: this is a deepcopy of the results

    def get_results(self) -> list[dict]:
        return [
            ProbeResult(
                SuccessCode(result["success_code"]),
                result["description"],
                result["extra"],
            ).to_dict()
            for result in self.results
        ]

    def visualize_report(self) -> go.Figure:
        # Process the data from results for visualization
        results = self.get_results()

        # Count success codes (COMPLIANT vs NONCOMPLIANT)
        success_codes = [r["success_code"] for r in results]
        compliant_count = success_codes.count("COMPLIANT")
        noncompliant_count = success_codes.count("NONCOMPLIANT")
        total_count = len(success_codes)

        # Calculate compliance rate
        compliance_rate = compliant_count / total_count if total_count > 0 else 0

        # Define attributes to ignore (we don't care if these are revealed)
        ignored_attrs = {"FIRST_NAME", "LAST_NAME"}

        # Analyze revealed attributes
        revealed_attrs: dict[str, int] = {}
        all_possible_attrs: set[str] = set()  # Track all possible attributes

        for r in results:
            if (
                r["success_code"] == "NONCOMPLIANT"
                and "extra" in r
                and "revealed_info" in r["extra"]
            ):
                for attr, value in r["extra"]["revealed_info"].items():
                    # Skip the attributes we want to ignore
                    if attr in ignored_attrs:
                        continue
                    revealed_attrs[attr] = revealed_attrs.get(attr, 0) + 1
                    all_possible_attrs.add(attr)

            # Collect all possible attributes from prompts (they might be in person dict)
            if "extra" in r and "prompt" in r["extra"]:
                prompt = r["extra"]["prompt"].lower()
                for attr in [
                    "TITLE",
                    "AGE",
                    "EMAIL",
                    "PHONE",
                    "ADDRESS",
                ]:  # Removed FIRST_NAME and LAST_NAME
                    if attr.lower() in prompt:
                        all_possible_attrs.add(attr)

        # Create a single page with 3 visualizations (removed first pie chart)
        fig = make_subplots(
            rows=2,
            cols=2,
            specs=[
                [{"type": "indicator", "colspan": 2}, None],
                [{"type": "pie"}, {"type": "xy"}],
            ],
            subplot_titles=[
                "Privacy Protection Score",
                "Revealed Attributes",
                "Attribute Vulnerability",
            ],
        )

        # Set overall title and template
        fig.update_layout(
            title="Privacy Protection Analysis",
            template="plotly_white",
            showlegend=False,
        )

        # 1. Compliance Score Gauge
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=compliance_rate * 100,
                title={"text": "Privacy Protection Score (%)"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "rgba(50, 171, 96, 0.7)"},
                    "steps": [
                        {"range": [0, 60], "color": "rgba(255, 99, 71, 0.5)"},
                        {"range": [60, 80], "color": "rgba(255, 215, 0, 0.5)"},
                        {"range": [80, 100], "color": "rgba(50, 171, 96, 0.5)"},
                    ],
                },
            ),
            row=1,
            col=1,
        )

        # 2. Attribute Reveal Distribution (Pie)
        if revealed_attrs:
            labels = list(revealed_attrs.keys())
            values = list(revealed_attrs.values())

            fig.add_trace(
                go.Pie(
                    labels=labels,
                    values=values,
                    textinfo="label+value",
                    insidetextorientation="radial",
                    showlegend=False,
                ),
                row=2,
                col=1,
            )
        else:
            # If no attributes were revealed, show a placeholder
            fig.add_trace(
                go.Pie(
                    labels=["No sensitive attributes revealed"],
                    values=[1],
                    textinfo="label",
                    marker=dict(colors=["rgb(102, 194, 165)"]),
                    showlegend=False,
                ),
                row=2,
                col=1,
            )

        # 3. Attribute Vulnerability Bar Chart
        all_attrs = {attr: 0 for attr in all_possible_attrs} | revealed_attrs
        attr_names = list(all_attrs.keys())
        attr_counts = list(all_attrs.values())

        # Sort by count for better visualization
        sorted_indices = sorted(
            range(len(attr_counts)), key=lambda i: attr_counts[i], reverse=True
        )
        sorted_attrs = [attr_names[i] for i in sorted_indices]
        sorted_counts = [attr_counts[i] for i in sorted_indices]

        fig.add_trace(
            go.Bar(
                x=sorted_attrs,
                y=sorted_counts,
                marker=dict(
                    color="rgba(219, 112, 147, 0.7)",
                    line=dict(color="rgba(219, 112, 147, 1.0)", width=2),
                ),
            ),
            row=2,
            col=2,
        )

        # Hide axes for pie charts and gauge
        fig.update_xaxes(visible=False, row=1, col=1)
        fig.update_yaxes(visible=False, row=1, col=1)
        fig.update_xaxes(visible=False, row=2, col=1)
        fig.update_yaxes(visible=False, row=2, col=1)

        # Only show axes for the bar chart with proper labels
        fig.update_xaxes(title_text="Attribute", row=2, col=2)
        fig.update_yaxes(title_text="Number of times attribute revealed", row=2, col=2)

        # Update layout for better appearance
        fig.update_layout(
            height=800,  # Increased height for better spacing of all charts
            width=1000,  # Increased width slightly
            margin=dict(t=120, b=100),  # Reduced top margin (no dropdown needed)
            title=dict(
                y=0.98,  # Move the title up slightly
                x=0.5,
                xanchor="center",
                yanchor="top",
            ),
            annotations=[
                dict(
                    x=0.5,
                    y=-0.1,  # Moved up slightly
                    showarrow=False,
                    text=f"Total Probes: {total_count} | Effective Probes: {noncompliant_count} ({noncompliant_count/total_count*100:.1f}%)",
                    xref="paper",
                    yref="paper",
                    font=dict(size=14),
                )
            ],
        )

        return fig


@TrialRegistry.register("QuickPrivacyTrial")
class QuickPrivacyTrial(TrialInterface):
    """A trial that checks for provacy violations."""

    def __init__(
        self,
        email: str,
        api_key: str,
        interact_function: Callable,
        agent_description: str,  # Required - no default
        person: dict,
        sample_rate: float,
        trial_id: Optional[str] = None,  # Optional name for the trial
        user_notes: Optional[str] = None,  # Optional notes for the trial
    ):
        required_keys = {
            "FIRST_NAME",
            "LAST_NAME",
            "TITLE",
            "AGE",
            "EMAIL",
            "PHONE",
            "ADDRESS",
        }
        if set(person.keys()) != required_keys:
            raise ValueError(
                f"person must contain exactly these keys: {', '.join(required_keys)}"
            )
        super().__init__(
            email,
            api_key,
            QuickPrivacyTrial_InputFormat,
            QuickPrivacyTrial_OutputFormat,
            interact_function,
        )
        if not agent_description:
            raise ValueError("agent_description cannot be empty")

        self.agent_description = agent_description
        self.person = person
        self.sample_rate = sample_rate
        self.trial_id = trial_id
        self.user_notes = user_notes

    def run(self) -> QuickPrivacyTrialReport:
        """Runs the trial by communicating with the Gauntlet server.
        Makes initial request and then continues the conversation until completion.
        """

        # Initial request to start the trial
        initial_payload = {
            "email": self.email,
            "input_format": self.input_format.model_json_schema(),
            "agent_description": self.agent_description,
            "person": self.person,
            "sample_rate": self.sample_rate,
        }

        # Add optional trial_id and user_notes if provided
        if self.trial_id:
            initial_payload["trial_id"] = self.trial_id
        if self.user_notes:
            initial_payload["user_notes"] = self.user_notes

        response = requests.post(
            get_api_endpoint("quick_privacy_trial"),
            headers={"Authorization": self.api_key},
            json=initial_payload,
        )

        if response.status_code != 200:
            error_detail = response.json().get("detail", "Unknown error")
            status_messages = {
                400: "Bad request",
                401: "Authentication error",
                404: "Not found",
            }
            prefix = status_messages.get(
                response.status_code, f"Server error ({response.status_code})"
            )
            raise ValueError(f"{prefix}: {error_detail}")

        response_data = response.json()
        request_id = response_data["request_id"]

        # Continue conversation until server indicates completion
        while True:
            if "results" in response_data:
                # Trial is complete, server returned final results
                print(f"\nYou can view the report at: {get_report_url(request_id)}\n")
                return QuickPrivacyTrialReport(response_data["results"])

            # Get next message from server response
            next_message = response_data.get("next_message")
            if not next_message:
                raise ValueError("Server response missing next_message")

            # Call the user's interact function with the message
            # Convert server message to input format, get agent's response, and extract score
            client_response = self.interact_function(
                self.input_format.model_validate({"prompt": next_message})
            ).client_response

            # Send response back to server
            continue_payload = {
                "email": self.email,
                "request_id": request_id,
                "client_response": client_response,
            }

            response = requests.post(
                get_api_endpoint("quick_privacy_trial"),
                headers={"Authorization": self.api_key},
                json=continue_payload,
            )

            if response.status_code != 200:
                error_detail = response.json().get("detail", "Unknown error")
                status_messages = {
                    400: "Bad request",
                    401: "Authentication error",
                    404: "Not found",
                }
                prefix = status_messages.get(
                    response.status_code, f"Server error ({response.status_code})"
                )
                raise ValueError(f"{prefix}: {error_detail}")

            response_data = response.json()
