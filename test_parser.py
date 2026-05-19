from backend.vlm.parser import parse_vlm_response

raw_output = """
{
  "medicine_name": ["Betaloc", "Dorzolamidum", "Cimetidine", "Oxprelol"],
  "dosage": ["100mg - 1 tab BID", "10 mg - 1 tab BID", "50 mg - 2 tabs TID", "50mg - 1 tab QD"],
  "food_instruction": null,
  "time": ["BID", "BID", "TID", "QD"],
  "duration_days": null
}
"""

result = parse_vlm_response(raw_output)

print(result)
