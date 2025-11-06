#%%
import json
import os

# Load original JSON
# Get current folder where script is running
current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)
# Go one level up to reach 'backend'
parent_dir = os.path.dirname(current_dir)
print(parent_dir)
current_dir = os.path.dirname(parent_dir)  # folder where this .py file is located
print(current_dir)
# Build path to the JSON file inside the 'data' folder
file_path = os.path.join(current_dir, "data", "uk_school_courses_Y1_to_Y11.json")
print(file_path)
#%%
#file_path = os.path.join(current_dir, "uk_school_courses_Y1_to_Y11.json")
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

documents = []

for year_data in data:
    year = year_data.get("year")
    key_stage = year_data.get("key_stage")
    age_range = year_data.get("age_range")
    foundation_subjects = ", ".join(year_data.get("foundation_subjects", []))

    for subject_info in year_data.get("core_subjects", []):
        subject = subject_info.get("subject")
        focus = subject_info.get("focus")

        doc = {
            "text": f"Year {year} {subject} focuses on {focus}.",
            "metadata": {
                "year": year,
                "key_stage": key_stage,
                "age_range": age_range,
                "subject": subject,
                "topic": focus,
                "foundation_subjects": foundation_subjects
            }
        }
        documents.append(doc)

# Wrap into target structure
new_data = {"documents": documents}

# Save final JSON
with open("uk_curriculam_converted30oct2025.json", "w", encoding="utf-8") as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)

print(f"✅ Converted {len(documents)} documents successfully.")

# %%
