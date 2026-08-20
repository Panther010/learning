import pandas as pd
import json
from shared.path_utils import get_project_root


class FewShotPosts:

    def __init__(self, file_path=get_project_root() / 'projects/linkedin-post-generator/data/processed_posts.json' ):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)
            df = pd.json_normalize(posts)
            df["length"] = df["line_count"].apply(self.length_category)
            all_tags = df["tags"].apply(lambda x: x).sum()
            self.unique_tags = set(list(all_tags))

            self.df = df

    def length_category(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_filtered_post(self, length, language, tag):
        df_filtered = self.df[
            (self.df['language'] == language) &
            (self.df['length'] == length) &
            (self.df['tags'].apply(lambda tags: tag in tags))
        ]

        return df_filtered.to_dict(orient="records")

    def get_tags(self):
        return self.unique_tags


if __name__ == "__main__":
    fs = FewShotPosts()
    posts = fs.get_filtered_post("Short", "English", "Job Search")
    print(posts)