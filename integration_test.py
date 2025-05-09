from eleven_labs import get_voice

import requests
import os


example_transcript = """
Good morning, Mrs. Lewis. What brings you in today?

Hi, Doctor. I've been having this tight, wheezy feeling in my chest for a few days now, especially at night. I also get short of breath when I climb stairs.

Have you experienced anything like this before?

Yes, I've had mild asthma in the past, but it hasn't bothered me in years—until now.

Any recent allergies, infections, or changes in your environment?

We did adopt a cat about two weeks ago. That might be it.

That could be a trigger. Based on your symptoms and history of asthma, I think you're having a mild asthma flare-up likely triggered by allergens. I'm going to prescribe you an albuterol inhaler. Use it as needed, especially before physical activity or if you experience shortness of breath.

Okay. How often can I use it?

No more than every 4-6 hours, and not more than two puffs at a time. If you're needing it more than twice a day for several days, come back or go to urgent care.

Got it. Thank you.

I'll send the prescription electronically to your pharmacy. Let me know if your symptoms get worse.
"""


if __name__ == "__main__":
    path = "conversation_file.mp3"

    if os.path.exists(path):
        file = open(path, "rb")
    else:
        voice = get_voice(example_transcript)
        file = open(path, "wb")
        file.write(voice)

    url = "http://127.0.0.1:5000/completeform"
    response = requests.post(url, files={"file": file})
    print(response)
    print(response.content)
