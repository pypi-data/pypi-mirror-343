import os
import openai
from shipyard_bp_utils import text as shipyard_utils

def main():
    original_script = shipyard_utils.content_file_injection(
        os.environ.get("CHATGPT_SCRIPT", "")
    )
    original_script_typed = shipyard_utils.content_file_injection(
        os.environ.get("CHATGPT_SCRIPT_TYPED", "")
    )
    exported_script = os.environ.get("CHATGPT_EXPORTED_FILE_NAME")

    openai.api_key = os.environ.get("CHATGPT_API_KEY")

    try:
        with open(original_script) as f:
            lines = f.read()
    except:
        lines = original_script_typed

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"Add comments to this code to make it more readable: {lines}",
            }
        ],
    )

    with open(exported_script, "w") as f:
        f.write(completion.choices[0].message.content)

if __name__ == "__main__":
    main()