import json

def parse_vlm_response(raw: str):

    empty = {
        "medicine_name": [],
        "dosage": [],
        "food_instruction": [],
        "intake": [],
        "duration_days": [],
    }

    if not raw:
        return empty

    raw = raw.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(raw)
    except Exception:
        return empty

    # If list of objects → merge safely
    if isinstance(data, list):
        merged = {
            "medicine_name": [],
            "dosage": [],
            "food_instruction": [],
            "intake": [],
            "duration_days": [],
        }

        for item in data:
            if not isinstance(item, dict):
                continue

            for key in merged:
                value = item.get(key)

                if isinstance(value, list):
                    merged[key].extend(value)
                elif value is not None:
                    merged[key].append(value)

        return merged

    # If single object
    if isinstance(data, dict):
        for key in empty:
            value = data.get(key)

            if value is None:
                data[key] = []
            elif not isinstance(value, list):
                data[key] = [value]

        return data

    return empty
