import os
import argparse

from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt
from call_function import available_functions, call_function


load_dotenv()

api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError(
        "OPENROUTER_API_KEY environment variable not found"
    )


def main():
    parser = argparse.ArgumentParser(description="AI Agent")

    parser.add_argument(
        "user_prompt",
        type=str,
        help="User prompt",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    args = parser.parse_args()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": args.user_prompt,
        },
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )

        if args.verbose and response.usage is not None:
            print(
                f"Prompt tokens: "
                f"{response.usage.prompt_tokens}"
            )
            print(
                f"Response tokens: "
                f"{response.usage.completion_tokens}"
            )

        message = response.choices[0].message

        # Save the assistant's response to the conversation.
        messages.append(message)

        # If the model wants tools, execute them and give
        # the results back to the model.
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(
                    tool_call,
                    verbose=args.verbose,
                )

                if not result_message.get("content"):
                    raise RuntimeError(
                        "Function call returned empty content"
                    )

                if args.verbose:
                    print(f"-> {result_message['content']}")

                messages.append(result_message)

            # Go around the loop again.
            # The LLM will now see the tool results.
            continue

        # No tool calls means the model is finished.
        print("Final response:")
        print(message.content)
        return

    print(
        "Error: Agent reached the maximum number "
        "of iterations without a final response."
    )
    raise SystemExit(1)


if __name__ == "__main__":
    main()
