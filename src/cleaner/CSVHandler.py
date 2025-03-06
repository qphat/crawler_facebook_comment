import csv
import os

class CSVHandler:
    def __init__(self, group_id, post_id, output_dir="output"):
        self.filename = f"{output_dir}/{group_id}_{post_id}.csv"
        os.makedirs(output_dir, exist_ok=True)  # Tạo thư mục nếu chưa có

    def save_raw_comments(self, comments):
        with open(self.filename, mode='w', newline='', encoding='utf-16') as file:
            writer = csv.writer(file)
            writer.writerow(["username", "comment"])  # Ghi tiêu đề
            for comment in comments:
                writer.writerow([comment["username"], comment["comment"]])

        print(f"Đã lưu {len(comments)} bình luận vào {self.filename}")

    def save_cleaned_comments(self, cleaned_df):
        cleaned_filename = self.filename.replace(".csv", "_cleaned.csv")
        cleaned_df.to_csv(cleaned_filename, index=False, encoding='utf-16')
        print(f"Dữ liệu đã làm sạch được lưu vào {cleaned_filename}")
