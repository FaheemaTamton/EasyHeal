


def extract_medicine_details(image_path):
    processed_image = preprocess_prescription(image_path)
    image_base64 = image_to_base64(processed_image)

    try:
        response = client.chat.completions.create(
            model="qwen2-vl-7b-instruct",  # match exactly what LM Studio shows
            temperature=0.1,
            max_tokens=500,
            messages=[
                {
                    "role": "system",
                    "content": """
You are a medical prescription extraction assistant.

Extract ALL medicines from the image.

Return ONLY valid JSON.

If multiple medicines exist, return a JSON array.

Format:

[
  {
    "medicine_name": ["string"],
    "dosage": ["string"],
    "food_instruction": [null],
    "intake": ["string"],
    "duration_days": [null]
  }
]

Do NOT explain.
Return JSON only.
"""
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract all medicines from this prescription."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]
        )

        content = response.choices[0].message.content

        print("=== MODEL RAW CONTENT ===")
        print(content)
        print("=========================")

        return content

    except Exception as e:
        print("VLM ERROR:", str(e))
        return None
