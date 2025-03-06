import re


class DataCleaner:
    def __init__(self, dataframe=None, text_column=None):
        self.dataframe = dataframe
        self.text_column = text_column

    def clean_comment(self, comment):
        """
        Làm sạch dữ liệu text cơ bản:
        - Xóa link.
        - Xóa emoji và ký tự đặc biệt.
        - Chuẩn hóa khoảng trắng.
        - Loại bỏ dữ liệu không cần thiết như số điện thoại, email.

        :param comment: Chuỗi văn bản cần làm sạch.
        :return: Chuỗi văn bản đã làm sạch hoặc None nếu chuỗi trống.
        """
        # 1. Xóa link
        comment = re.sub(r"http\S+|www\S+|https\S+", "", comment, flags=re.MULTILINE)

        # 2. Xóa emoji và ký tự đặc biệt (chỉ giữ lại chữ, số, khoảng trắng, dấu câu cơ bản)
        comment = re.sub(r"[^\w\s.,!?]", "", comment)

        # 3. Chuẩn hóa khoảng trắng
        comment = re.sub(r"\s+", " ", comment).strip()

        # 4. Chuyển văn bản về chữ thường
        comment = comment.lower()

        # 5. Loại bỏ dữ liệu không cần thiết
        comment = re.sub(r"\b\d{9,10}\b", "", comment)  # Loại bỏ số điện thoại
        comment = re.sub(r"\S+@\S+\.\S+", "", comment)  # Loại bỏ email

        return comment if comment else None

    def apply_cleaning(self):
        """
        Áp dụng làm sạch dữ liệu trên toàn bộ cột text trong DataFrame.
        """
        self.dataframe[self.text_column] = (
            self.dataframe[self.text_column]
            .astype(str)
            .apply(self.clean_comment)
        )

        # Xóa dòng bị trống sau khi làm sạch
        self.dataframe = self.dataframe.dropna(subset=[self.text_column])

        # Xóa các dòng trùng lặp
        self.dataframe = self.dataframe.drop_duplicates(subset=[self.text_column])

    def get_cleaned_data(self):
        """
        Trả về DataFrame đã làm sạch.
        """
        return self.dataframe


def apply_cleaning():
    return None