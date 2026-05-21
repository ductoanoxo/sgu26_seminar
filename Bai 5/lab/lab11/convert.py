import json

# Giả sử file của bạn là data_openai.jsonl
input_file = "fine_tuning.jsonl"
output_file = "data_gemini.json"

gemini_data = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)
        # Chỉ lấy những mẫu có trọng số 1
        if item["messages"][-1].get("weight") == 0:
            continue
            
        messages = item["messages"]
        system_msg = messages[0]["content"]
        user_msg = messages[1]["content"]
        assistant_msg = messages[-1]["content"]

        # Gộp System và User vào một lượt hội thoại của người dùng
        combined_input = f"{system_msg}\n\n{user_msg}"
        
        gemini_entry = {
            "contents": [
                {"role": "user", "parts": [{"text": combined_input}]},
                {"role": "model", "parts": [{"text": assistant_msg}]}
            ]
        }
        gemini_data.append(gemini_entry)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(gemini_data, f, ensure_ascii=False, indent=2)

print(f"Đã chuyển đổi xong! Bạn có thể upload file {output_file} lên AI Studio.")