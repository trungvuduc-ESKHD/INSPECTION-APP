# Eurofins Inspection System
Hệ thống giám định Eurofins

## Cấu trúc dự án / Project Structure

```
├── main.py                          # Entry point chính / Main entry point
├── requirements.txt                 # Dependencies
├── src/                            # Source code chính / Main source code
│   ├── config/                     # Cấu hình / Configuration
│   │   ├── __init__.py
│   │   └── app_config.py          # Cấu hình ứng dụng / App configuration
│   ├── core/                      # Chức năng cốt lõi / Core functionality
│   │   ├── __init__.py
│   │   ├── session_manager.py     # Quản lý session / Session management
│   │   └── data_manager.py        # Quản lý dữ liệu / Data management
│   ├── styles/                    # Styling và theme / Styling and theming
│   │   ├── __init__.py
│   │   └── theme.py              # Theme và CSS / Theme and CSS
│   └── ui/                        # Giao diện người dùng / User interface
│       ├── __init__.py
│       ├── components/            # Components tái sử dụng / Reusable components
│       │   ├── __init__.py
│       │   └── ui_helpers.py      # Helper functions cho UI / UI helper functions
│       ├── layout/                # Layout components
│       │   ├── __init__.py
│       │   ├── header.py          # Header layout
│       │   └── footer.py          # Footer layout
│       ├── tabs/                  # Tab implementations
│       │   ├── __init__.py
│       │   ├── tabs_controller.py # Main tabs controller
│       │   ├── general_tab.py     # General information tab
│       │   ├── quality_tab.py     # Quality inspection tab
│       │   ├── weight_tab.py      # Weight sampling tab
│       │   └── defects_tab.py     # Defects assessment tab
│       └── forms/                 # Form components
│           ├── __init__.py
│           ├── product_form.py    # Product information form
│           └── container_status_form.py # Container status form
```

## Cách chạy / How to run

1. Cài đặt dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Chạy ứng dụng:
   ```bash
   streamlit run main.py
   ```

## Tính năng / Features

- ✅ Thông tin chung / General Information
- ✅ Thông tin sản phẩm / Product Information  
- ✅ Trạng thái container / Container Status
- ✅ Giám định chất lượng / Quality Inspection
- ✅ Lấy mẫu cân nặng / Weight Sampling
- ✅ Đánh giá lỗi / Defects Assessment
- ✅ Lưu/Tải dữ liệu JSON / Save/Load JSON data
- ✅ Giao diện song ngữ / Bilingual interface

## Công nghệ sử dụng / Technologies Used

- Streamlit
- Pandas
- Python 3.10+
