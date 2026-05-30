import http from 'k6/http';
import { check, group, sleep } from 'k6';

const BASE_URL = 'http://localhost:5249/Khoa';
const headers = {
  'Content-Type': 'application/json',
};

export default function () {
  group('Khoa API Test', () => {
    // 1. Gửi GET danh sách
    const getRes = http.get(BASE_URL);
    check(getRes, {
      'GET /Khoa trả về 200': (r) => r.status === 200,
      'GET /Khoa có dữ liệu dạng array': (r) => Array.isArray(r.json()),
    });

    // 2. Gửi POST tạo mới
    const khoaData = {
      maKhoa: '',
      tenKhoa: `Khoa Test ${Math.random().toString(36).substring(2, 6)}`,
      viTri: 'Tầng 2',
      tenVietTat: `KT${Math.floor(Math.random() * 1000)}`,
      moTa: 'Đây là khoa kiểm thử',
    };

    const postRes = http.post(BASE_URL, JSON.stringify(khoaData), { headers });
    check(postRes, {
      'POST /Khoa trả về 201': (r) => r.status === 201,
    });

    const created = postRes.json();

    if (created && created.id) {
      // 3. Gửi PUT cập nhật thông tin
      const updatedData = {
        id: created.id,
        maKhoa: created.maKhoa || '',
        tenKhoa: created.tenKhoa + ' - Updated',
        viTri: 'Tầng 3',
        tenVietTat: created.tenVietTat + 'U',
        moTa: 'Mô tả mới sau cập nhật',
      };

      const putRes = http.put(BASE_URL, JSON.stringify(updatedData), { headers });
      check(putRes, {
        'PUT /Khoa cập nhật thành công': (r) => r.status === 200,
      });

      // 4. Xoá bản ghi
      const delRes = http.del(`${BASE_URL}/${created.id}`);
      check(delRes, {
        'DELETE /Khoa/:id thành công': (r) => r.status === 204 || r.status === 200,
      });
    }

    sleep(1); // nghỉ 1s cho mỗi vòng
  });
}
