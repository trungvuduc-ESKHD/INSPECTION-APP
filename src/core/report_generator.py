import streamlit as st
from fpdf import FPDF
import datetime
import os
from decimal import Decimal, InvalidOperation
from PIL import Image
from io import BytesIO

class PDF(FPDF):
    def setup_fonts(self):
        font_dir = os.path.join(os.path.dirname(__file__), '..', 'fonts')
        self.add_font('DejaVu', '', os.path.join(font_dir, 'DejaVuSans.ttf'), uni=True)
        self.add_font('DejaVu', 'B', os.path.join(font_dir, 'DejaVuSans-Bold.ttf'), uni=True)
        self.add_font('DejaVu', 'I', os.path.join(font_dir, 'DejaVuSans-Oblique.ttf'), uni=True)
        self.font_name = 'DejaVu'
        self.logo_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'eurofins_logo.png')

    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font(self.font_name, 'I', 8)
        self.cell(w=0, h=10, txt=str(self.page_no()), border=0, ln=0, align='R')

    def _draw_bordered_kv(self, label, value, width, height, border=1):
        x, y = self.get_x(), self.get_y()
        self.set_font(self.font_name, '', 8)
        self.multi_cell(w=width, h=height / 2, txt=label, border='LTR', align='L')
        self.set_xy(x, y + height / 2)
        self.set_font(self.font_name, 'B', 9)
        self.multi_cell(w=width, h=height / 2, txt=str(value), border='LBR', align='L')
        self.set_xy(x + width, y)

    def _draw_multiline_header(self, width, height, text, border=1, align='C', fill=False):
        x, y = self.get_x(), self.get_y()
        self.multi_cell(w=width, h=height, txt="", border=border, align=align, fill=fill)
        lines = text.split('\n')
        line_height_text = 4.5
        total_text_height = len(lines) * line_height_text
        y_text = y + (height - total_text_height) / 2
        self.set_xy(x, y_text)
        self.multi_cell(w=width, h=line_height_text, txt=text, border=0, align=align)
        self.set_xy(x + width, y)

    def draw_page_1(self, data):
        self.add_page()
        if os.path.exists(self.logo_path):
            self.image(self.logo_path, x=10, y=8, w=40)
        self.set_y(15)
        self.set_font(self.font_name, 'B', 14)
        self.cell(w=0, h=10, txt='INSPECTION REPORT', border=0, ln=1, align='C')
        
        top_box_y = self.get_y()
        self.set_xy(120, top_box_y)
        self.set_font(self.font_name, 'B', 9)
        self.cell(w=30, h=7, txt='Document No:', border=1)
        self.set_font(self.font_name, '', 9)
        self.cell(w=50, h=7, txt=data['generalInfo'].get('documentNo', ''), border=1, ln=1)
        self.set_x(120)
        self.set_font(self.font_name, 'B', 9)
        self.cell(w=30, h=7, txt='Version No:', border=1)
        self.set_font(self.font_name, '', 9)
        self.cell(w=50, h=7, txt=str(data['generalInfo'].get('versionNo', '')), border=1, ln=1)
        self.set_x(120)
        self.set_font(self.font_name, 'B', 9)
        self.cell(w=30, h=7, txt='Published on:', border=1)
        self.set_font(self.font_name, '', 9)
        self.cell(w=50, h=7, txt=data['generalInfo'].get('publishedDate', ''), border=1, ln=1)
        self.set_x(120)
        self.set_font(self.font_name, 'B', 10)
        self.set_fill_color(217, 83, 79)
        self.set_text_color(255, 255, 255)
        self.cell(w=30, h=7, txt='Order No', border=1, align='C', fill=True)
        self.set_text_color(0, 0, 0)
        self.set_font(self.font_name, 'B', 9)
        self.set_fill_color(240, 240, 240)
        self.cell(w=50, h=7, txt=data['generalInfo'].get('orderNo', ''), border=1, ln=1, fill=True)

        self.set_y(top_box_y + 35)
        self.set_font(self.font_name, 'B', 11)
        self.set_fill_color(220, 220, 220)
        self.cell(w=0, h=8, txt='Thông tin chung/General information', border=1, ln=1, align='L', fill=True)
        
        cell_height = 12
        y_start_info = self.get_y()
        self._draw_bordered_kv('Nguồn gốc - Tên nhà cung cấp', data['generalInfo'].get('supplierName', ''), 95, cell_height)
        self._draw_bordered_kv('Tên khách hàng', data['generalInfo'].get('customerName', ''), 95, cell_height)
        self.set_xy(10, y_start_info + cell_height)
        self._draw_bordered_kv('Số hợp đồng', data['generalInfo'].get('contractNumber', ''), 95, cell_height)
        self._draw_bordered_kv('Tổng lượng kiện được nhận (carton)', data['generalInfo'].get('receivedQuantity', ''), 95, cell_height)
        self.set_xy(10, y_start_info + 2 * cell_height)
        self._draw_bordered_kv('Số container/ xe lạnh', data['generalInfo'].get('containerNumber', ''), 95, cell_height)
        self._draw_bordered_kv('Ngày hàng đến/ ETA', data['generalInfo'].get('eta', ''), 95, cell_height)
        self.set_xy(10, y_start_info + 3 * cell_height)
        self._draw_bordered_kv('Bộ phận chịu trách nhiệm', data['generalInfo'].get('department', ''), 95, cell_height)
        self._draw_bordered_kv('Kiểm hàng bởi', data['generalInfo'].get('inspectedBy', ''), 95, cell_height)
        self.set_xy(10, y_start_info + 4 * cell_height)
        self._draw_bordered_kv('Địa điểm kiểm hàng', data['generalInfo'].get('location', ''), 95, cell_height)
        self._draw_bordered_kv('Ngày kiểm hàng', data['generalInfo'].get('inspectionDate', ''), 95, cell_height)
        self.set_y(y_start_info + 5 * cell_height)

        self.ln(5)
        self.set_font(self.font_name, 'B', 11)
        self.set_fill_color(220, 220, 220)
        self.cell(w=0, h=8, txt='Thông tin về sản phẩm/ Product information', border=1, ln=1, align='L', fill=True)
        self.set_fill_color(240, 240, 240)
        self.set_font(self.font_name, 'B', 8)
        self._draw_multiline_header(10, 12, 'No', align='C', fill=True)
        self._draw_multiline_header(60, 12, 'Tên sản phẩm\nProduct name', align='C', fill=True)
        self._draw_multiline_header(25, 12, 'Kích cỡ\nSize', align='C', fill=True)
        self._draw_multiline_header(50, 12, 'Số lượng túi được nhận\nReceived quantity of bag', align='C', fill=True)
        self._draw_multiline_header(45, 12, 'Khối lượng tịnh (Kgs)\nNet Weight (Kgs)', align='C', fill=True)
        self.ln(12)
        self.set_font(self.font_name, '', 9)
        for i, p in enumerate(data.get('products', [])):
            self.cell(w=10, h=7, txt=str(i + 1), border=1, align='C')
            self.cell(w=60, h=7, txt=p.get('name', ''), border=1, align='L')
            self.cell(w=25, h=7, txt=p.get('size', ''), border=1, align='C')
            self.cell(w=50, h=7, txt=str(p.get('receivedQuantity', '')), border=1, align='C')
            self.cell(w=45, h=7, txt=str(p.get('netWeight', '')), border=1, ln=1, align='C')
        
        self.ln(5)
        self.set_font(self.font_name, 'B', 11)
        self.set_fill_color(220, 220, 220)
        self.cell(w=0, h=8, txt='Tình trạng phương tiện vận chuyển/ Container status', border=1, ln=1, align='L', fill=True)
        y = self.get_y()
        self.set_font(self.font_name, 'B', 8)
        self.set_fill_color(240, 240, 240)
        self._draw_multiline_header(130, 10, 'Chỉ tiêu đánh giá\nFeature', align='C', fill=True)
        self.set_font(self.font_name, 'B', 9)
        self.set_text_color(255, 0, 0)
        self._draw_multiline_header(60, 10, 'Kết quả kiểm → Đánh dấu "X"\nResults → Mark "X"', align='C', fill=True)
        self.set_text_color(0, 0, 0)
        self.set_xy(140, y + 5)
        self.set_font(self.font_name, 'B', 8)
        self.cell(w=30, h=5, txt='Tốt/OK', border=1, align='C', fill=True)
        self.cell(w=30, h=5, txt='Không tốt/Not OK', border=1, ln=1, align='C', fill=True)
        self.set_y(y + 10)
        self.set_font(self.font_name, '', 9)
        for item in data.get('containerStatus', []):
            status = item.get('isOk')
            ok_mark, not_ok_mark = ('', '')
            if status is True: ok_mark = 'X'
            elif status is False: not_ok_mark = 'X'
            elif status is None: ok_mark = 'N/A'
            self.cell(w=130, h=7, txt=item.get('feature', ''), border=1, align='L')
            self.cell(w=30, h=7, txt=ok_mark, border=1, align='C')
            self.cell(w=30, h=7, txt=not_ok_mark, border=1, ln=1, align='C')

    def draw_quality_recap_page(self, data):
        self.add_page()
        self.set_y(15)
        self.set_font(self.font_name, 'B', 12)
        self.set_fill_color(217, 83, 79) # Màu đỏ
        self.set_text_color(255, 255, 255)
        self.cell(w=0, h=8, txt='TỔNG HỢP GIÁM ĐỊNH CHẤT LƯỢNG / QUALITY INSPECTION RECAP', border=0, ln=1, align='C', fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(5)
        
        # === Bảng 1: Product Specifications ===
        self.set_font(self.font_name, 'B', 9)
        self.set_fill_color(220, 220, 220)
        self.cell(w=0, h=7, txt='1. Những đặc điểm kỹ thuật của sản phẩm/ Product specifications', border=1, ln=1, align='L', fill=True)
        
        headers1 = ['STT', 'Tên sản phẩm', 'Kích cỡ', 'Đặc điểm của giống\ntrái/ Variety', 'Mọng nước', 'Độ Brix', 'Độ cứng']
        # --- ĐIỀU CHỈNH CHIỀU RỘNG CỘT CHO BẢNG 1 ---
        col_widths1 = [10, 60, 20, 40, 20, 20, 20] # Tổng = 190
        header_height1 = 20
        
        self.set_font(self.font_name, 'B', 8)
        self.set_fill_color(240, 240, 240)
        y_header = self.get_y()
        for i, h in enumerate(headers1):
            self._draw_multiline_header(col_widths1[i], header_height1, h, fill=True)
        self.set_y(y_header + header_height1)
        
        self.set_font(self.font_name, '', 9)
        for i, p in enumerate(data.get('products', [])):
            self.cell(w=col_widths1[0], h=7, txt=str(i + 1), border=1, align='C')
            self.cell(w=col_widths1[1], h=7, txt=p.get('name', ''), border=1, align='L')
            self.cell(w=col_widths1[2], h=7, txt=p.get('size', ''), border=1, align='C')
            self.cell(w=col_widths1[3], h=7, txt=p.get('varietyCharacteristics', 'OK'), border=1, align='C')
            self.cell(w=col_widths1[4], h=7, txt=p.get('juicyLevel', 'OK'), border=1, align='C')
            self.cell(w=col_widths1[5], h=7, txt=str(p.get('brixDegree', '')), border=1, align='C')
            self.cell(w=col_widths1[6], h=7, txt=str(p.get('firmness', '')), border=1, ln=1, align='C')
        self.ln(5)

        # === Bảng 2: Net weight checking recap ===
        self.set_font(self.font_name, 'B', 9)
        self.set_fill_color(220, 220, 220)
        self.cell(w=0, h=7, txt='2. Tổng hợp thông tin về kiểm tra khối lượng tịnh/ Net weight checking recap', border=1, ln=1, align='L', fill=True)
        
        headers2 = ['STT', 'Tên sản phẩm', 'Kích cỡ', 'Khối lượng tịnh trung bình\n(kg)', 'Mục tiêu (Kg)', 'Status']
        # --- ĐIỀU CHỈNH CHIỀU RỘNG CỘT CHO BẢNG 2 ---
        col_widths2 = [10, 60, 20, 40, 20, 40] # Tổng = 190
        header_height2 = 20
        
        self.set_font(self.font_name, 'B', 8)
        self.set_fill_color(240, 240, 240)
        y_header = self.get_y()
        for i, h in enumerate(headers2):
            self._draw_multiline_header(col_widths2[i], header_height2, h, fill=True)
        self.set_y(y_header + header_height2)
        
        self.set_font(self.font_name, '', 9)
        for i, p in enumerate(data.get('products', [])):
            self.cell(w=col_widths2[0], h=7, txt=str(i + 1), border=1, align='C')
            self.cell(w=col_widths2[1], h=7, txt=p.get('name', ''), border=1, align='L')
            self.cell(w=col_widths2[2], h=7, txt=p.get('size', ''), border=1, align='C')
            self.cell(w=col_widths2[3], h=7, txt=str(data.get('weightSampling', {}).get(str(p.get('id')), {}).get('averageWeight', '')), border=1, align='C')
            self.cell(w=col_widths2[4], h=7, txt=str(data.get('weightSampling', {}).get(str(p.get('id')), {}).get('targetWeight', '')), border=1, align='C')
            self.cell(w=col_widths2[5], h=7, txt=p.get('weightStatus', 'C'), border=1, ln=1, align='C')
        self.ln(5)

        # === Bảng 3: Defects assessment recap ===
        self.set_font(self.font_name, 'B', 9)
        self.set_fill_color(220, 220, 220)
        self.cell(w=0, h=7, txt='3. Tổng hợp thông tin về đánh giá các lỗi/ Defects assessment recap', border=1, ln=1, align='L', fill=True)
        
        headers3 = ['STT', 'Tên sản phẩm', 'Kích cỡ', 'Tổng Lỗi nghiêm trọng\n(%)', 'Tổng Lỗi Lớn\n(%)', 'Tổng Lỗi nhẹ\n(%)', 'Tổng Quả Bị Rụng\n(%)']
        # --- ĐIỀU CHỈNH CHIỀU RỘNG CỘT CHO BẢNG 3 ---
        col_widths3 = [10, 60, 20, 40, 20, 20, 20] # Tổng = 190
        header_height3 = 20
        
        self.set_font(self.font_name, 'B', 8)
        self.set_fill_color(240, 240, 240)
        y_header = self.get_y()
        for i, h in enumerate(headers3):
            self._draw_multiline_header(col_widths3[i], header_height3, h, fill=True)
        self.set_y(y_header + header_height3)
        
        self.set_font(self.font_name, '', 9)
        for i, p in enumerate(data.get('products', [])):
            defects = data.get('defectAssessment', {}).get(str(p.get('id')), {})
            self.cell(w=col_widths3[0], h=7, txt=str(i + 1), border=1, align='C')
            self.cell(w=col_widths3[1], h=7, txt=p.get('name', ''), border=1, align='L')
            self.cell(w=col_widths3[2], h=7, txt=p.get('size', ''), border=1, align='C')
            self.cell(w=col_widths3[3], h=7, txt=f"{float(defects.get('seriousDefectsPercentage', '0')):.4f}%", border=1, align='C')
            self.cell(w=col_widths3[4], h=7, txt=f"{float(defects.get('majorDefectsPercentage', '0')):.4f}%", border=1, align='C')
            self.cell(w=col_widths3[5], h=7, txt=f"{float(defects.get('minorDefectsPercentage', '0')):.4f}%", border=1, align='C')
            self.cell(w=col_widths3[6], h=7, txt=f"{float(defects.get('shatteringBerriesPercentage', '0')):.4f}%", border=1, ln=1, align='C')

    def draw_weight_sampling_page(self, product, weight_data):
        self.add_page()
        self.set_y(15)
        
        # --- Header ---
        self.set_font(self.font_name, 'B', 11)
        self.set_fill_color(220, 220, 220)
        self.cell(w=0, h=8, txt='KẾ HOẠCH LẤY MẪU & KIỂM TRA KHỐI LƯỢNG / SAMPLING PLAN & WEIGHT CHECKING', border=1, ln=1, align='C', fill=True)
        
        # --- Thông tin sản phẩm ---
        self.set_font(self.font_name, 'B', 10)
        self.set_fill_color(217, 83, 79) # Màu đỏ
        self.set_text_color(255, 255, 255)
        self.cell(w=0, h=7, txt=f"Sản phẩm / Product: {product.get('name', '')} ({product.get('size', '')})", border=1, ln=1, align='C', fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

        # --- Thông tin lấy mẫu ---
        self.set_font(self.font_name, 'B', 9)
        self.cell(w=95, h=7, txt='Kế hoạch lấy mẫu/ Sampling plan', border=1)
        self.cell(w=95, h=7, txt='Số hộp/Qty. of bags', border=1, ln=1)
        self.set_font(self.font_name, '', 9)
        self.cell(w=95, h=7, txt=f"{weight_data.get('samplingPlan', '')} túi/bags", border=1)
        self.cell(w=95, h=7, txt=f"{weight_data.get('bags', '')} bags", border=1, ln=1)
        self.ln(2)

        # --- Khối lượng túi rỗng (LAYOUT MỚI) ---
        self.set_font(self.font_name, 'B', 6)
        self.cell(w=80, h=7, txt='Khối lượng của túi rỗng (3 túi)\nEmpty weight of bag (3 bags)', border=1, align='C')
        
        ew_values = weight_data.get('emptyBagWeights', ['', '', ''])
        ew_avg = weight_data.get('emptyBagWeightAverage', '')
        
        self.set_font(self.font_name, '', 7)
        self.set_fill_color(255, 255, 0) # Màu vàng
        self.cell(w=20, h=7, txt=str(ew_values[0]), border=1, align='C', fill=True)
        self.cell(w=20, h=7, txt=str(ew_values[1]), border=1, align='C', fill=True)
        self.cell(w=20, h=7, txt=str(ew_values[2]), border=1, align='C', fill=True)
        
        self.set_fill_color(255, 255, 255) # Reset màu nền
        self.set_font(self.font_name, 'B', 7)
        self.cell(w=30, h=7, txt='Trung bình/ Average', border=1, align='C')
        self.set_font(self.font_name, '', 6)
        self.cell(w=20, h=7, txt=str(ew_avg), border=1, align='C')
        self.cell(w=0, h=7, txt='Kgs', border=1, ln=1, align='C')
        self.ln(4)

        # --- Bảng Gross Weight ---
        self.set_font(self.font_name, 'B', 9)
        self.set_fill_color(192, 192, 192) # Light grey for title
        self.cell(0, 7, 'Khối lượng tổng cộng của mỗi túi có tính bao bì (Kg)/ Gross weight per bag (Kg)', 1, 1, 'C', fill=True)
        self._draw_weight_grid(weight_data.get('samples', []), 'grossWeight')

        # --- Bảng Net Weight ---
        self.set_font(self.font_name, 'B', 9)
        self.set_fill_color(192, 192, 192)
        self.cell(0, 7, 'Khối lượng tổng cộng của mỗi túi có trừ bao bì (Kg)/ Net weight per bag (Kg)', 1, 1, 'C', fill=True)
        self._draw_weight_grid(weight_data.get('samples', []), 'netWeight')
        
        # --- Tổng hợp ---
        self.set_font(self.font_name, 'B', 8)
        self.cell(80, 7, 'Tổng khối lượng có bì/ Total gross weight', 1, 0)
        self.set_font(self.font_name, '', 8)
        self.cell(30, 7, str(weight_data.get('totalGrossWeight', '')), 1, 0, 'C')
        self.cell(0, 7, 'Kgs', 1, 1)

        self.set_font(self.font_name, 'B', 8)
        self.cell(80, 7, 'Tổng khối lượng trừ bì/ Total net weight', 1, 0)
        self.set_font(self.font_name, '', 8)
        self.cell(30, 7, str(weight_data.get('totalNetWeight', '')), 1, 0, 'C')
        self.cell(0, 7, 'Kgs', 1, 1)

        self.set_font(self.font_name, 'B', 8)
        self.cell(80, 7, 'Khối lượng tịnh trung bình/ Average of net weight', 1, 0)
        self.set_font(self.font_name, '', 8)
        self.cell(30, 7, str(weight_data.get('averageWeight', '')), 1, 0, 'C')
        self.cell(30, 7, 'Target[]))', 1, 0, 'C')
        self.cell(30, 7, str(weight_data.get('targetWeight', '')), 1, 0, 'C')
        self.cell(0, 7, 'Kgs', 1, 1)

    def _draw_weight_grid(self, samples, key):
        self.set_font(self.font_name, 'B', 6)
        self.set_fill_color(220, 220, 220)
        self.cell(19, 6, 'Mẫu/ Samples', 1, 0, 'C', fill=True)
        for i in range(10):
            self.cell(17.1, 6, str(i+1), 1, 0, 'C', fill=True)
        self.ln()

        self.set_font(self.font_name, '', 8)
        col_width_data = 17.1
        col_width_label = 19
        for i in range(4):
            self.set_font(self.font_name, 'B', 7)
            self.cell(col_width_label, 6, f'{i*10+1}-{i*10+10}', 1, 0, 'C')
            self.set_font(self.font_name, '', 8)
            for j in range(10):
                sample_index = i * 10 + j
                if sample_index < len(samples):
                    value = samples[sample_index].get(key, '')
                    self.cell(col_width_data, 6, str(value), 1, 0, 'C')
                else:
                    self.cell(col_width_data, 6, '', 1, 0, 'C')
            self.ln()
        self.ln(4)

    def draw_defects_assessment_page(self, product, detailed_defects):
        self.add_page()
        self.set_y(10)

        # --- Header chính của trang ---
        self.set_font(self.font_name, 'B', 10)
        y_start_header = self.get_y()
        self.multi_cell(w=40, h=5, txt='INSPECTION FINDINGS', border=1, align='C')
        self.set_xy(50, y_start_header)
        self.multi_cell(w=60, h=5, txt='Tên sản phẩm\nProduct name', border=1, align='C')
        self.set_xy(110, y_start_header)
        self.multi_cell(w=60, h=10, txt=product.get('name', ''), border=1, align='C')
        self.set_xy(170, y_start_header)
        self.multi_cell(w=30, h=5, txt='Kích cỡ\nSize', border=1, align='C')
        self.set_xy(170, y_start_header + 5)
        self.multi_cell(w=30, h=5, txt=product.get('size', ''), border='LBR', align='C')
        self.set_y(y_start_header + 10)

        self.set_font(self.font_name, 'B', 10)
        self.set_fill_color(220, 220, 220)
        self.cell(w=0, h=5, txt='ĐÁNH GIÁ CÁC LỖI TRÊN SẢN PHẨM/ DEFECTS ASSESSMENT', border=1, ln=1, align='C', fill=True)
        self.ln(1)

        # --- Vẽ từng bảng lỗi ---
        self._draw_defect_table('Các nghiêm trọng / Serious defects', detailed_defects.get('seriousDefects', []))
        self._draw_defect_table('Các lỗi lớn/ Major defects', detailed_defects.get('majorDefects', []))
        self._draw_defect_table('Các lỗi nhỏ/ Minor defects', detailed_defects.get('minorDefects', []))
        self._draw_defect_table('Quả bị rụng cuống/ Shattering (Loosing) berries', detailed_defects.get('shatteringBerries', []))

    def _draw_defect_table(self, title, defects_list):
        line_height = 4 

        # Header của loại lỗi
        self.set_font(self.font_name, 'B', 10)
        self.set_fill_color(240, 240, 240)
        self.cell(w=0, h=7, txt=title, border=1, ln=1, align='C', fill=True)

        # Header của bảng
        col_widths = {'type': 45, 'desc': 105, 'weight': 20, 'percent': 20}
        self.set_font(self.font_name, 'B', 8)
        self.set_fill_color(245, 245, 245)
        y_header = self.get_y()
        self._draw_multiline_header(col_widths['type'], 10, 'Loại lỗi\nType of Defective Goods', fill=True)
        self._draw_multiline_header(col_widths['desc'], 10, 'Mô tả\nDetail', fill=True)
        self._draw_multiline_header(col_widths['weight'], 10, 'Khối lượng\n(Kg)', fill=True)
        self._draw_multiline_header(col_widths['percent'], 10, 'Phần trăm\n(%)', fill=True)
        self.set_y(y_header + 10)

        # Dữ liệu bảng
        total_weight = Decimal('0.0')
        total_percent = Decimal('0.0')
        
        if not defects_list:
            self.cell(sum(col_widths.values()), 7, 'Không có dữ liệu', 1, 1, 'C')
        else:
            for defect in defects_list:
                defect_type_key = defect.get('defectType', '').upper()
                weight_str = str(defect.get('weight', '')).strip() or "0"
                percent_str = str(defect.get('percentage', '')).strip().replace('%', '') or "0"
                
                try:
                    total_weight += Decimal(weight_str)
                    if percent_str != "Lỗi": total_percent += Decimal(percent_str)
                except InvalidOperation: pass

                # --- TÍNH TOÁN CHIỀU CAO ĐỘNG VÀ ÁP DỤNG HỆ SỐ NHÂN ---
                start_y = self.get_y()
                x_pos = self.get_x()

                # Tính chiều cao dự kiến cho ô mô tả
                self.set_font(self.font_name, '', 7)
                self.multi_cell(col_widths['desc'], line_height, defect.get('description', ''), border=0, align='L', dry_run=True)
                calculated_height = self.get_y() - start_y
                self.set_y(start_y)

                # Xác định hệ số nhân chiều cao dựa trên loại lỗi
                height_multiplier = 1.0 # Giá trị mặc định
                if 'SERIOUS DEFECTS' in defect_type_key:
                    height_multiplier = 2.4
                elif 'MAJOR 1' in defect_type_key:
                    height_multiplier = 3.6
                elif 'MAJOR 2' in defect_type_key:
                    height_multiplier = 4.6
                elif 'MAJOR 3' in defect_type_key:
                    height_multiplier = 4.1
                elif 'VẾT DA' in defect_type_key:
                    height_multiplier = 2.4
                elif 'SHATTERING' in defect_type_key:
                    height_multiplier = 1.9
                
                # Chiều cao cuối cùng của hàng
                row_height = max(calculated_height, 7) * height_multiplier
                row_height = max(row_height, 10) # Đảm bảo chiều cao tối thiểu cuối cùng là 10

                # --- VẼ NỘI DUNG VÀ VIỀN ---
                self.rect(x_pos, start_y, col_widths['type'], row_height)
                self.rect(x_pos + col_widths['type'], start_y, col_widths['desc'], row_height)
                self.rect(x_pos + col_widths['type'] + col_widths['desc'], start_y, col_widths['weight'], row_height)
                self.rect(x_pos + col_widths['type'] + col_widths['desc'] + col_widths['weight'], start_y, col_widths['percent'], row_height)

                self.set_xy(x_pos, start_y + (row_height - 10)/2)
                self.set_font(self.font_name, 'B', 8)
                self.multi_cell(col_widths['type'], 5, defect.get('defectType', ''), border=0, align='C')
                
                self.set_xy(x_pos + col_widths['type'], start_y + 1)
                self.set_font(self.font_name, '', 7)
                self.multi_cell(col_widths['desc'], line_height, defect.get('description', ''), border=0, align='L')
                
                self.set_xy(x_pos + col_widths['type'] + col_widths['desc'], start_y + (row_height - 5)/2)
                self.set_font(self.font_name, '', 8)
                self.multi_cell(col_widths['weight'], 5, weight_str, border=0, align='R')
                
                self.set_xy(x_pos + col_widths['type'] + col_widths['desc'] + col_widths['weight'], start_y + (row_height - 5)/2)
                self.multi_cell(col_widths['percent'], 5, f"{float(percent_str):.4f}%" if percent_str else "0.0000%", border=0, align='R')

                self.set_y(start_y + row_height)

        # Dòng tổng
        self.set_font(self.font_name, 'B', 9)
        self.cell(col_widths['type'] + col_widths['desc'], 7, f'TỔNG / TOTAL', 1, 0, 'R')
        self.cell(col_widths['weight'], 7, f"{total_weight:.3f}", 1, 0, 'R')
        self.cell(col_widths['percent'], 7, f"{total_percent:.4f}%", 1, 1, 'R')
        self.ln(4)

    def draw_final_page(self, data):
        self.add_page()
        self.set_y(15)
        self.set_font(self.font_name, 'B', 11)
        self.set_fill_color(220, 220, 220)
        self.cell(w=0, h=8, txt='Nhận xét chung/ Comments', border=1, ln=1, align='L', fill=True)
        self.set_font(self.font_name, '', 9)
        comments = data.get('comments', 'Noted:')
        self.multi_cell(w=0, h=5, txt=comments, border=1, align='L')
        self.ln(10)
        
        self.set_font(self.font_name, 'B', 9)
        self.set_fill_color(240, 240, 240)
        self.cell(w=95, h=7, txt="Name(s) of Inspector(s)", border=1, align='C', fill=True)
        self.cell(w=95, h=7, txt="Name of Reviewer", border=1, ln=1, align='C', fill=True)
        
        y_sign = self.get_y()
        self.cell(w=95, h=40, txt="", border=1)
        self.cell(w=95, h=40, txt="", border=1, ln=1)
        
        self.set_font(self.font_name, 'B', 10)
        self.set_y(y_sign + 30)
        self.cell(w=95, h=7, txt=data.get('inspectorName', ''), border=0, align='C')
        self.set_y(y_sign + 30)
        self.set_x(105)
        self.cell(w=95, h=7, txt=data.get('reviewerName', ''), border=0, align='C')
        self.ln(5)
        self.set_font(self.font_name, '', 9)
        self.set_x(105)
        self.cell(w=95, h=7, txt='INSPECTION MANAGER', border=0, align='C')

    def draw_final_page(self, data):
        self.add_page()
        self.set_y(15)
        self.set_font(self.font_name, 'B', 11)
        self.set_fill_color(220, 220, 220)
        self.cell(w=0, h=8, txt='Nhận xét chung/ Comments', border=1, ln=1, align='L', fill=True)
        self.set_font(self.font_name, '', 9)
        comments = data.get('comments', 'Noted:')
        self.multi_cell(w=0, h=5, txt=comments, border=1, align='L')
        self.ln(10)
        
        self.set_font(self.font_name, 'B', 9)
        self.set_fill_color(240, 240, 240)
        self.cell(w=95, h=7, txt="Name(s) of Inspector(s)", border=1, align='C', fill=True)
        self.cell(w=95, h=7, txt="Name of Reviewer", border=1, ln=1, align='C', fill=True)
        
        y_sign = self.get_y()
        # Vẽ 2 ô trống cho chữ ký
        self.cell(w=95, h=40, txt="", border=1)
        self.cell(w=95, h=40, txt="", border=1, ln=1)
        
        # --- LOGIC CHÈN ẢNH CHỮ KÝ ---
        # Chữ ký Inspector
        if data.get('inspector_signature') is not None:
            try:
                # Chuyển dữ liệu ảnh numpy array sang Pillow Image
                img = Image.fromarray(data['inspector_signature'])
                # Lưu vào memory buffer dưới dạng PNG để giữ nền trong suốt (nếu có)
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                buffer.seek(0)
                # Chèn ảnh vào PDF, giữ tỉ lệ
                self.image(buffer, x=20, y=y_sign + 5, w=65)
            except Exception as e:
                print(f"Error embedding inspector signature: {e}")

        # Chữ ký Reviewer
        if data.get('reviewer_signature') is not None:
            try:
                img = Image.fromarray(data['reviewer_signature'])
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                buffer.seek(0)
                self.image(buffer, x=120, y=y_sign + 5, w=65)
            except Exception as e:
                print(f"Error embedding reviewer signature: {e}")
        # -----------------------------

        # In tên và chức vụ
        self.set_font(self.font_name, 'B', 10)
        self.set_y(y_sign + 30)
        self.cell(w=95, h=7, txt=data.get('inspectorName', ''), border=0, align='C')
        self.set_y(y_sign + 30)
        self.set_x(105)
        self.cell(w=95, h=7, txt=data.get('reviewerName', ''), border=0, align='C')
        self.ln(5)
        self.set_font(self.font_name, '', 9)
        self.set_x(105)
        self.cell(w=95, h=7, txt='INSPECTION MANAGER', border=0, align='C')


# --- HÀM CHÍNH ĐỂ TẠO BÁO CÁO PDF ---
def generate_pdf_report(inspection_data: dict) -> bytes:
    try:
        pdf = PDF('P', 'mm', 'A4')
        pdf.setup_fonts()
        pdf.alias_nb_pages()

        pdf.draw_page_1(inspection_data)
        pdf.draw_quality_recap_page(inspection_data)
        
        products = inspection_data.get('products', [])
        for product in products:
            product_id_str = str(product.get('id'))
            
            weight_data = inspection_data.get('weightSampling', {}).get(product_id_str)
            if weight_data:
                pdf.draw_weight_sampling_page(product, weight_data)

            detailed_defects = inspection_data.get('detailedDefectAssessment', {}).get(product_id_str)
            if detailed_defects:
                pdf.draw_defects_assessment_page(product, detailed_defects)

        pdf.draw_final_page(inspection_data)

        return bytes(pdf.output())

    except Exception as e:
        st.error(f"Lỗi khi tạo PDF: {e}")
        import traceback
        traceback.print_exc()
        return None