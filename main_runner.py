from eleven_labs import get_text
from pdf_handling import build_structured_form

import asyncio


template = """
    Pre-Authorization Form (if applicable):

    Prescribed Test or Medication:

    Reason for Prescription:

    Medical Diagnosis or ICD-10 Code (if mentioned or inferable):

    Additional Notes for Insurance:
"""


async def process(audio: bytes) -> str:
    transcript = get_text(audio)
    return await build_structured_form(template, transcript)



