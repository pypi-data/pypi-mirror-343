import json
import sys
from typing import Any, IO, Optional

from geewiz.progress import ProgressContext, ProgressIncrementer, ProgressState


class GeewizClient:
    last_card_attrs: Optional[dict] = None

    def __init__(self, input: IO[str] = sys.stdin, output: IO[str] = sys.stdout):
        self.input = input
        self.output = output
        self.variables = Variables(self)
        self.var = Var(self.variables)
        self.progress = ProgressIncrementer()
        self.progress.on_update = self.update_progress

    def update_progress(self, progress_state: ProgressState, context=ProgressContext):
        context = context or {}
        self.var.progress = progress_state

        if not context.get("dont_resend_card"):
            self.resend_last_card()

    def set_input(self, input: IO[str]):
        self.input = input

    def set_output(self, output: IO[str]):
        self.output = output

    def set(self, title: str):
        self.command("set", title=title)

    def var_command(self, name: str, value: Any):
        self.command("var", name=name, value=value)
        return value

    def card(
        self,
        id: Optional[str] = None,
        var: Optional[dict] = None,
        steps: Optional[int] = None,
        **kwargs: Any,
    ):
        id_kwargs = {"id": id} if id else {}

        if steps is not None:
            self.progress.reset(steps, context={"dont_resend_card": True})

        var = var or {}
        for name, value in var.items():
            self.variables[name] = value

        attrs = dict(**kwargs, **id_kwargs)

        self.command("card", **attrs, responseFormat="json")

        self.last_card_attrs = attrs

        return self.read_response()

    def read_response(self):
        response = self.input.readline()
        return json.loads(response)

    def resend_last_card(self):
        if self.last_card_attrs is not None:
            return self.card(**self.last_card_attrs)

    def get_user_config(self, key: str):
        self.command("get-user-config", key=key, responseFormat="json")
        return self.read_response()

    def command(self, command: str, **kwargs: Any):
        self.output.write(f"\n@{GeewizJsonEncoder().encode([command, kwargs])}\n")
        self.output.flush()


class Variables(dict):
    def __init__(self, client: GeewizClient):
        super().__init__()
        self.client = client

    def __setitem__(self, key, value):
        self.client.var_command(key, value)
        super().__setitem__(key, value)

    # TODO: implement 'update' and other methods that modify items


class Var:
    def __init__(self, cache: Variables):
        super().__setattr__("cache", cache)

    def __getattr__(self, name):
        return self.cache[name]

    def __setattr__(self, name, value):
        self.cache[name] = value

    def __getitem__(self, name):
        return self.cache[name]

    def __setitem__(self, name, value):
        self.cache[name] = value


class GeewizJsonEncoder(json.JSONEncoder):
    """Custom JSON encoder for Geewiz objects."""

    def default(self, o):
        if hasattr(o, "as_json"):
            return o.as_json()

        if hasattr(o, "__dict__"):
            return o.__dict__

        return super().default(o)
