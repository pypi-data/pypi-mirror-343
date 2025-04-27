## Cài đặt
```python
pip install skinidaov
```
## Giới thiệu
- `skinidaov` có 2 hàm gồm `to_standard(int/str)`  và `to_base(int/str)`.
- Base (cơ bản) trong `to_base()` dùng để chỉ dạng id ngoại hình trang phục (skin) và cũng là id được ghi trên dữ liệu trang phục.
- Standard (chuẩn) trong `to_standard()` dủng để chỉ dạng id hiệu ứng, hình ảnh và âm thanh.
## Cách dùng
```python
import skinidaov
base_id = "1505"
standard_id = skinidaov.to_standard(base_id)
print(standard_id) #kết quả 15004

standard_id2 = "14110"
base_id2 = skinidaov.to_base(standard_id2)
print(base_id2) #kết quả 1419
```
## Thông tin tác giả
© Thư viên do [Ron AOV](https://youtube.com/@ronaov) thực hiện