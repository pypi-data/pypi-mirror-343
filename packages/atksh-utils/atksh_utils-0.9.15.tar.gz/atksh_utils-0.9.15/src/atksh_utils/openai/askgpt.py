#!/usr/bin/env python3
import argparse
import os
import readline
from concurrent.futures import ThreadPoolExecutor as TPE
from functools import partial

from atksh_utils.openai import OpenAI
from atksh_utils.openai.tool import parse_args

blue = "\033[34m"
green = "\033[32m"
red = "\033[31m"
bold = "\033[1m"
gray = "\033[90m"
reset = "\033[0m"


tokens = []
executor = TPE(max_workers=1)


def cb(chunk, message, verbose: bool = False, openai: OpenAI = None):
    global tokens, executor

    def print_tokens():
        global tokens
        if len(tokens) == 0:
            return
        text = "".join(tokens)
        try:
            has_break = text.endswith("\n")
            if not text.endswith("\n") and has_break:
                text += "\n"
        except:
            pass
        print(f"{green}{text}{reset}", end="")
        tokens.clear()
        if openai:
            executor.submit(openai.speech, text)

    if (finish_reason := chunk.choices[0].dict().get("finish_reason")) is not None:
        if finish_reason == "stop":
            print_tokens()
            print("\n")
        else:
            info = chunk.choices[0].dict()
            if info["finish_reason"] == "tool_calls":
                print_tokens()
                n_calls = len(message.tool_calls)
                if verbose:
                    print(f"\n\n{bold}{blue}Calling {n_calls} function(s){reset}{blue}:")
                for i in range(len(message.tool_calls)):
                    function_name = message.tool_calls[i].function.name
                    if verbose:
                        print(message.tool_calls[i].function)
                    try:
                        function_call_args = parse_args(message.tool_calls[i].function.arguments)
                    except ValueError:
                        if verbose:
                            print("Error: JSONDecodeError", end=": ")
                            print(message.tool_calls[i].function.arguments)
                    else:
                        pretty_args = []
                        if isinstance(function_call_args, str):
                            if verbose:
                                print(f"{bold}{red}Error{reset}{red}: {function_call_args}{reset}")
                        else:
                            for arg, value in function_call_args.items():
                                value = str(value).replace("\n", "\n" + " " * len(arg) + " " * 3)
                                pretty_args.append(f"  {arg}={value}")
                            pretty_args = ",\n".join(pretty_args)
                            text = f"\n{reset}{bold}{blue}{function_name}{reset}{blue}(\n{pretty_args}\n)\n\n"
                            if verbose:
                                print(text + reset)
    token = chunk.choices[0].delta.content
    if token:
        tokens.append(token)
        if token.endswith("\n"):
            print_tokens()


def setup_ai(use_4o: bool, use_4_1: bool) -> OpenAI:
    """
    Create an OpenAI client based on model flags.
    Priority: GPT-4o if use_4o, else GPT-4.1 if use_4_1, else GPT-4.1-mini.
    """
    key = os.getenv("OPENAI_API_KEY")
    if use_4o:
        model = "gpt-4o-2024-11-20"
    elif use_4_1:
        model = "gpt-4.1"
    else:
        model = "gpt-4.1-mini"
    ai = OpenAI(key, model)
    ai.set_utility_functions()
    ai.set_browser_functions()
    ai.set_bash_function()
    ai.set_python_functions()
    return ai


def ask():
    os.environ["ASKGPT_VERBOSE"] = "0"
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", help="Verbose mode.")
    parser.add_argument("--enable-speech", action="store_true", help="Enable speech.")
    parser.add_argument("--use-4o", action="store_true", help="Use GPT-4o model.")
    parser.add_argument(
        "--use-4.1",
        dest="use_4_1",
        action="store_true",
        help="Use GPT-4.1 model (otherwise GPT-4.1-mini).",
    )
    args = parser.parse_args()
    verbose = args.verbose
    if verbose:
        os.environ["ASKGPT_VERBOSE"] = "1"
    ai = setup_ai(args.use_4o, args.use_4_1)
    not_called = True
    user_prompt = None
    try:
        while True:
            empty_input_count = 0
            lines = []
            lines.append(
                input(
                    f"{reset}{gray}Continue the conversation. To send your reply, "
                    f"please press Enter more than three times.{reset}\n>>> "
                )
            )
            while empty_input_count < 3:
                try:
                    lines.append(input(">>> "))
                    user_prompt = "\n".join(lines).strip()
                    if not lines[-1].strip():
                        empty_input_count += 1
                        continue
                    else:
                        empty_input_count = 0
                except (KeyboardInterrupt, EOFError):
                    user_prompt = None
                    break
            if user_prompt:
                if not_called:
                    user_prompt = (
                        user_prompt
                        + "\n---\n[system message]\tThink carefully and plan to answer the input within the <thoughts> tag before answering within the <final_answer> tag at first."
                    )
                if not_called:
                    print(f"\n{bold}{red}AI{reset}{red}: {bold}{blue}Thinking...{reset}\n")
                    messages, _ = ai(
                        user_prompt,
                        stream_callback=partial(
                            cb, verbose=verbose, openai=ai if args.enable_speech else None
                        ),
                    )
                    not_called = False
                else:
                    print(f"\n{bold}{red}AI{reset}{red}: {bold}{blue}Thinking...{reset}\n")
                    ai.try_call(
                        user_prompt,
                        stream_callback=partial(
                            cb, verbose=verbose, openai=ai if args.enable_speech else None
                        ),
                        messages=messages,
                    )
                user_prompt = None
            else:
                while True:
                    y_or_n = (
                        input(f"{reset}{gray}Do you want to quit? (y/n): {reset}").strip().lower()
                    )
                    if y_or_n == "y":
                        print("\n")
                        print(f"{reset}{gray}Bye!{reset}")
                        return
                    elif y_or_n == "n":
                        break
                    else:
                        print(
                            f"{reset}{gray}{y_or_n} is not a valid input. Please try again.{reset}"
                        )
    except (KeyboardInterrupt, EOFError):
        print("\n")
        print(f"{reset}{gray}Bye!{reset}")
