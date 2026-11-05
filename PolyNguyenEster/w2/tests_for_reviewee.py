import pytest
from datetime import date

# Import các module tuần 1 (W1) từ thư mục của nhatduyhuynh1-ops
from python_bootcamp.nhatduyhuynh1.w1 import grades, rules, text_tools, timetable, translate

def test_nhatduy_grades():
    """Kiểm thử hàm summary/grades của nhatduyhuynh1-ops."""
    # Giả định hàm summary nhận danh sách điểm
    if hasattr(grades, "summary"):
        res = grades.summary([7.0, 8.5, 9.0])
        assert res["max"] == 9.0
        assert res["min"] == 7.0

def test_nhatduy_text_tools():
    """Kiểm thử hàm đếm từ (word_count / top_k) của nhatduyhuynh1-ops."""
    if hasattr(text_tools, "word_count"):
        counts = text_tools.word_count("Git is fast. Git is cool!")
        assert counts.get("git", 0) == 2

def test_nhatduy_rules():
    """Kiểm thử điều kiện đăng ký đồ án tốt nghiệp (can_register_thesis)."""
    if hasattr(rules, "can_register_thesis"):
        assert rules.can_register_thesis(130, 2.5) is True
        assert rules.can_register_thesis(100, 2.5) is False

def test_nhatduy_translate():
    """Kiểm thử phần dịch thuật toán C++ sang Python của nhatduyhuynh1-ops."""
    if hasattr(translate, "binary_search"):
        arr = [1, 3, 5, 7, 9]
        assert translate.binary_search(arr, 5) == 2
        assert translate.binary_search(arr, 4) == -1

def test_nhatduy_timetable():
    """Kiểm thử hàm gom nhóm thời khóa biểu của nhatduyhuynh1-ops."""
    if hasattr(timetable, "by_day"):
        data = [("CSC10014", "Mon"), ("MTH00003", "Tue")]
        result = timetable.by_day(data)
        assert "Mon" in result
        assert "CSC10014" in result["Mon"]

def test_edge_case_negative_threshold_or_empty():
    """Trường hợp biên bổ sung (edge case) để đảm bảo không bị crash khi dữ liệu rỗng."""
    if hasattr(text_tools, "word_count"):
        assert text_tools.word_count("") == {}