import os
from typing import Any, Literal, Type, cast

from anthropic import Anthropic
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from together import Together  # type: ignore

load_dotenv()


class Chatbot:
    def __init__(self, llm: str, system_prompt: str):
        self.client: Any
        if llm.startswith(("gpt", "o1", "o3")):
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif llm.startswith("claude"):
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        elif "llama" in llm:
            self.client = Together(api_key=os.getenv("TOGETHERAI_API_KEY"))
        else:
            raise ValueError(f"Unsupported LLM: {llm}")
        self.llm = llm
        self.messages = [{"role": "system", "content": system_prompt}]

    def add_message(self, role: Literal["user", "assistant"], message: str) -> None:
        self.messages.append({"role": role, "content": message})

    def _get_completion_response(self) -> str:
        if isinstance(self.client, (OpenAI, Together)):
            return self._handle_openai_togetherai_completion()
        elif isinstance(self.client, Anthropic):
            return self._handle_anthropic_completion()
        raise ValueError(f"Something went wrong with the client for {self.llm}")

    def _handle_openai_togetherai_completion(self) -> str:
        completion = self.client.chat.completions.create(
            model=self.llm, messages=self.messages
        )
        if completion.choices[0].message.content is None:
            raise ValueError("No content in the response")
        return str(completion.choices[0].message.content)

    def _handle_anthropic_completion(self) -> str:
        completion = self.client.messages.create(
            model=self.llm,
            system=self.messages[0]["content"],
            max_tokens=4096,
            messages=[
                {"role": m["role"], "content": m["content"]} for m in self.messages[1:]
            ],
        )
        if completion.usage is None:
            raise ValueError("No usage in the response")
        return str(completion.content[0].text)

    def get_response(self, prompt: str) -> str:
        self.add_message("user", prompt)
        response_content = self._get_completion_response()
        self.messages.append({"role": "assistant", "content": response_content})
        return response_content

    def get_structured_response(
        self, prompt: str, output_format: Type[BaseModel]
    ) -> BaseModel:
        self.add_message("user", prompt)
        completion = self.client.beta.chat.completions.parse(
            model=self.llm,
            messages=self.messages,
            response_format=output_format,
        )
        if completion.choices[0].message.parsed is None:
            raise ValueError("No parsed content in the response")
        self.messages.append(
            {
                "role": "assistant",
                "content": completion.choices[0].message.parsed.model_dump_json(),
            }
        )
        return cast(BaseModel, completion.choices[0].message.parsed)
