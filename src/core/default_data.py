# src/core/default_data.py
import datetime

def get_fixed_defects_structure():
    """Cung cấp cấu trúc lỗi cố định."""
    return {
        "seriousDefects": [
            {"defectType": "LỖI NGHIÊM TRỌNG/ SERIOUS DEFECTS", "description": "Sự suy giảm hoặc biến đổi...", "weight": "", "percentage": ""}
        ],
        "majorDefects": [
            {"defectType": "MAJOR 1 DEFECTS", "description": "HƯ HỎNG DO CÔN TRÙNG...", "weight": "", "percentage": ""},
            {"defectType": "MAJOR 2 DEFECTS", "description": "HƯ HỎNG VẬT LÝ...", "weight": "", "percentage": ""},
            {"defectType": "MAJOR 3 DEFECTS", "description": "VẾT DA/KHUYẾT TẬT...", "weight": "", "percentage": ""}
        ],
        "minorDefects": [
            {"defectType": "TỔN THƯƠNG VẬT LÝ/ PHYSICAL DAMAGE", "description": "- Vết tổn thương trên vỏ quả <0.5cm2", "weight": "", "percentage": ""},
            {"defectType": "VẾT DA/KHUYẾT TẬT/ SKIN MARKS/ BLEMISHES", "description": "- Quả bị da cám...", "weight": "", "percentage": ""}
        ],
        "shatteringBerries": [
            {"defectType": "SHATTERING (LOOSING) BERRIES", "description": "- Quả phải đặc trưng của loại...", "weight": "", "percentage": ""}
        ]
    }

def get_default_inspection_data():
    """Cung cấp một "template" dữ liệu trống cho một báo cáo mới."""
    return {
        'generalInfo': {
            'documentNo': 'EHC-TP8.4-02/F01', 'versionNo': '1', 'department': 'INSPECTION',
            'inspectedBy': 'EUROFINS VN', 'publishedDate': datetime.datetime.now().strftime('%d.%m.%Y'),
            'orderNo': '', 'supplierName': '', 'customerName': '', 'contractNumber': '',
            'receivedQuantity': '', 'containerNumber': '', 'eta': None, 'location': '',
            'inspectionDate': None, 'report_name': '', 'report_id': ''
        },
        'products': [],
        'containerStatus': [
            {"feature": "Phương tiện sạch sẽ?/Container is clean?", "isOk": None},
            {"feature": "Hệ thống thông gió hoạt động tốt?/Ventilation system is ok?", "isOk": None},
            {"feature": "Không rò rỉ?/No leakage?", "isOk": None},
            {"feature": "Thiết bị ghi nhiệt hoạt động tốt?/Temperature recorder is good?", "isOk": None},
            {"feature": "Tình trạng kiện hàng (móp méo, hư hại)?/Package status (deformed, damaged)?", "isOk": None},
            {"feature": "Mùi lạ?/Any abnormal smell?", "isOk": None},
            {"feature": "Nhiệt độ của phương tiện khi đến nơi?/Container temperature upon arrival?", "isOk": None},
        ],
        'defectAssessment': {},
        'detailedDefectAssessment': {},
        'weightSampling': {},
        'comments': '', 'qualityComments': '',
        'inspectorName': '', 'reviewerName': '',
        'inspector_signature': None, 'reviewer_signature': None,

    }
