<h1>
  <p align="center">
    Movie Analytics

  </p>
</h1>

Kho lưu trữ này chứa mã nguồn và tài nguyên cho dự án Movie Analytics.

## Cấu trúc dự án

Dự án được tổ chức thành các thư mục sau:

- **data:** Chứa các tệp dữ liệu được sử dụng trong dự án:
  - **movies.csv:** Chứa dữ liệu thô được thu thập từ nguồn.
  - **cleaned_movies.csv:** Chứa dữ liệu đã được làm sạch sau khi tiền xử lý.
  - **cleaned_movies_no_outliers.csv:** Chứa dữ liệu đã được làm sạch và loại bỏ các giá trị ngoại lai.
- **environments:** 
  - Chứa tệp `requirements.txt` để thiết lập môi trường Python.
- **notebooks:** 
  - Chứa các sổ tay Jupyter để khám phá và phân tích dữ liệu (EDA).
  - Mô hình:
    - **Model_Movie_Profitability_Predictor.ipynb:** Chứa mã huấn luyện mô hình dự đoán lợi nhuận của phim.
    - **Model_Optimize_Budget.ipynb:** Chứa mã huấn luyện mô hình tối ưu hóa ngân sách cho phim.
    - **Model_Optimize_Budget:** Chứa mã huấn luyện mô hình tối ưu hóa ngân sách cho phim.
- **scripts:** Chứa các tập lệnh cho các tác vụ khác nhau (ví dụ: thu thập dữ liệu, huấn luyện mô hình).
- **src:** Chứa mã nguồn của dự án.
  - **preprocess.ipynb:** Chứa mã xử lý dữ liệu.
  - **crawler:** Chứa mã thu thập dữ liệu.

## Các tệp

- **.env:** Tệp chứa các biến môi trường.
- **.gitignore:** Chỉ định các tệp và thư mục cần bỏ qua khi sử dụng Git để quản lý phiên bản.
- **.pre-commit-config.yaml:** Cấu hình cho các hooks trước khi commit.

## Cài đặt

### Cài đặt môi trường 
```
cd environments
pip install -r requirements.txt
```