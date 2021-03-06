import sys

import prompt_toolkit.patch_stdout

from questionary import utils
from questionary.constants import DEFAULT_KBI_MESSAGE
from typing import Any


class Question:
    """A question to be prompted.

    This is an internal class. Questions should be created using the
    predefined questions (e.g. text or password)."""

    def __init__(self, application: prompt_toolkit.Application):
        self.application = application
        self.should_skip_question = False
        self.default = None

    async def ask_async(self,
                        patch_stdout: bool = False,
                        kbi_msg: str = DEFAULT_KBI_MESSAGE) -> Any:
        """Ask the question using asyncio and return user response."""

        if self.should_skip_question:
            return self.default

        try:
            sys.stdout.flush()
            return await self.unsafe_ask_async(patch_stdout)
        except KeyboardInterrupt:
            print("\n{}\n".format(kbi_msg))
            return None

    def ask(self,
            patch_stdout: bool = False,
            kbi_msg: str = DEFAULT_KBI_MESSAGE) -> Any:
        """Ask the question synchronously and return user response."""

        if self.should_skip_question:
            return self.default

        try:
            return self.unsafe_ask(patch_stdout)
        except KeyboardInterrupt:
            print("\n{}\n".format(kbi_msg))
            return None

    def unsafe_ask(self, patch_stdout: bool = False) -> Any:
        """Ask the question synchronously and return user response.

        Does not catch keyboard interrupts."""

        if patch_stdout:
            with prompt_toolkit.patch_stdout.patch_stdout():
                return self.application.run()
        else:
            return self.application.run()

    def skip_if(self, condition: bool, default: Any = None) -> 'Question':
        """Skip the question if flag is set and return the default instead."""

        self.should_skip_question = condition
        self.default = default
        return self

    async def unsafe_ask_async(self, patch_stdout: bool = False) -> Any:
        """Ask the question using asyncio and return user response.

        Does not catch keyboard interrupts."""

        if not utils.ACTIVATED_ASYNC_MODE:
            await utils.activate_prompt_toolkit_async_mode()

        if patch_stdout:
            # with prompt_toolkit.patch_stdout.patch_stdout():
            return await self.application.run_async().to_asyncio_future()
        else:
            return await self.application.run_async().to_asyncio_future()
