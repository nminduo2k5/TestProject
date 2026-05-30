import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 10,
  duration: '20s',
};

const BASE_URL = 'http://localhost:5249/HeSoLopHocPhan';
const CURRENT_YEAR = new Date().getFullYear();

export default function () {
  // 1. GET tất cả hệ số lớp học phần
  const getAll = http.get(BASE_URL);
  check(getAll, {
    'GET /HeSoLopHocPhan trả về 200': (r) => r.status === 200,
  });

  // 2. GET theo năm → nếu chưa có thì tạo mặc định
  const getByYear = http.get(`${BASE_URL}/${CURRENT_YEAR}`);
  check(getByYear, {
    [`GET /HeSoLopHocPhan/${CURRENT_YEAR} trả về 200`]: (r) => r.status === 200,
  });

  // 3. POST tạo mới hệ số lớp
  const payload = JSON.stringify({
    soHocSinhToiThieu: Math.floor(Math.random() * 100) + 10,
    heSo: Math.round((Math.random() * 2 + 1) * 100) / 100,
    namHoc: CURRENT_YEAR,
  });

  const headers = { 'Content-Type': 'application/json' };
  const postRes = http.post(BASE_URL, payload, { headers });

  check(postRes, {
    'POST /HeSoLopHocPhan trả về 200': (r) => r.status === 200,
  });

  // 4. Lấy lại danh sách để chuẩn bị sửa và xóa
  const getAfterPost = http.get(`${BASE_URL}/${CURRENT_YEAR}`);
  const list = getAfterPost.json();

  const created = list.find(i => i.namHoc === CURRENT_YEAR && i.soHocSinhToiThieu === JSON.parse(payload).soHocSinhToiThieu);

  if (created && created.id) {
    const updatedPayload = JSON.stringify({
      soHocSinhToiThieu: created.soHocSinhToiThieu + 5,
      heSo: created.heSo + 0.5,
      namHoc: CURRENT_YEAR,
    });

    // 5. PUT cập nhật hệ số lớp
    const putRes = http.put(`${BASE_URL}/${created.id}`, updatedPayload, { headers });
    check(putRes, {
      'PUT /HeSoLopHocPhan/:id trả về 200': (r) => r.status === 200,
    });

    // 6. DELETE hệ số lớp đã tạo
    const delRes = http.del(`${BASE_URL}/${created.id}`);
    check(delRes, {
      'DELETE /HeSoLopHocPhan/:id trả về 204 hoặc 200': (r) =>
        r.status === 204 || r.status === 200,
    });
  }

  sleep(1);
}
