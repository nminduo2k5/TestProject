import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 50,
  duration: '25s',
};

const BASE_URL = 'http://localhost:5249/BangCap';

function randomTenVietTat() {
  return Math.random().toString(36).substring(2, 6).toUpperCase();
}

export default function () {
  // 1. Lấy danh sách bằng cấp hiện có
  const getRes = http.get(BASE_URL);
  check(getRes, {
    'GET /BangCap trả về 200': (r) => r.status === 200,
  });

  // 2. Gửi POST thêm bằng cấp mới
  const uniqueId = `${Date.now()}_${Math.random().toString(36).substring(2, 8)}`;
  const newData = {
    maBangCap: `BC_${uniqueId}`,
    tenBangCap: `Bang Cap ${uniqueId}`,
    tenVietTat: `BCP${Math.random().toString(36).substring(2, 5).toUpperCase()}`
  };

  const headers = { 'Content-Type': 'application/json' };
  const postRes = http.post(BASE_URL, JSON.stringify(newData), { headers });

  check(postRes, {
    'POST /BangCap thành công': (r) => r.status === 201,
  });

  const created = postRes.json();

  if (created && created.id) {
    // 3. Gửi PUT cập nhật thông tin
    const updatedData = {
      id: created.id,
      maBangCap: created.maBangCap || '', // Có thể server gán mã, nếu không thì bỏ qua
      tenBangCap: created.tenBangCap + ' Updated',
      tenVietTat: created.tenVietTat + 'U',
    };

    const putRes = http.put(BASE_URL, JSON.stringify(updatedData), { headers });
    check(putRes, {
      'PUT /BangCap cập nhật thành công': (r) => r.status === 200,
    });

    // 4. Xoá bằng cấp vừa tạo
    const delRes = http.del(`${BASE_URL}/${created.id}`);
    check(delRes, {
      'DELETE /BangCap/:id thành công': (r) => r.status === 204 || r.status === 200,
    });
  }

  sleep(1);
}
