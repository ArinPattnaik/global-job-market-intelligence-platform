
import pandas as pd

skills_list = [
"python","sql","power bi","tableau","excel","machine learning",
"statistics","pandas","numpy","spark","aws","data visualization"
]

def extract_skills(text):
    text = str(text).lower()
    found = []
    for s in skills_list:
        if s in text:
            found.append(s)
    return ",".join(found)

def process():
    df = pd.read_csv("data/jobs_raw.csv")
    df["skills"] = df["description"].apply(extract_skills)
    df.to_csv("data/jobs_processed.csv", index=False)
    print("Skills extracted")

if __name__ == "__main__":
    process()
