import datetime
import uuid

def parse_date(date_input):
    """
    Parse date from string or datetime object.
    Returns a datetime object or None if parsing fails.
    """
    if not date_input:
        return None
        
    # Nếu đã là datetime object, trả về luôn
    if isinstance(date_input, datetime.datetime):
        return date_input
    if isinstance(date_input, datetime.date):
        return datetime.datetime.combine(date_input, datetime.datetime.min.time())

    # Nếu là chuỗi, thử các định dạng khác nhau
    if isinstance(date_input, str):
        formats = [
            '%Y-%m-%d',         # 2024-06-27
            '%d.%m.%Y',         # 27.06.2024
            '%d/%m/%Y',         # 27/06/2024
            '%Y-%m-%dT%H:%M:%S.%f', # ISO format có microsecond
            '%Y-%m-%dT%H:%M:%S'      # ISO format không có microsecond
        ]
        for fmt in formats:
            try:
                return datetime.datetime.strptime(date_input, fmt)
            except (ValueError, TypeError):
                continue

    # Nếu không thể parse, trả về None
    return None
def generate_id():
    """
    Creates a unique ID using a combination of timestamp and a random element.
    This is more robust than just timestamp.
    """
    # Sử dụng UUID4 để đảm bảo tính duy nhất cao
    return str(uuid.uuid4())