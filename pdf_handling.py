import os
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),  # This is the default and can be omitted
)


def build_prompt(template: str, data: str) -> str:
    return f"""
            You are a medical documentation assistant. Below is a transcript of a conversation between a doctor and a patient.
            Your task is to read and analyze the transcript and determine if the doctor prescribed any medical test(s) or medication(s).

            If yes, complete the pre-authorization form with the appropriate information extracted from the transcript.

            If no test or medication is prescribed, respond only with: "No pre-auth form need detected."

            Transcript:
            {data}

            Pre Authorization Form (if applicable):
            {template}
            """


async def build_structured_form(template: str, data: str) -> str:
    """
    [TextBlock(citations=None, text='Hello! How can I help you today?', type='text')]
    """
    message = await client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": build_prompt(template, data),
            }
        ],
        model="claude-3-5-sonnet-latest",
    )
    output = message.content[0].text
    print(f"Log Claude output: {output}")
    return output


asyncio.run(build_structured_form("make your own template", "prescribing you potatos twice a day"))
