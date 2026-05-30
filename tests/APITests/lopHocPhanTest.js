import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 50,
  duration: '30s',
  thresholds: {
    http_req_duration: ['p(95)<3000'],
    http_req_failed: ['rate<0.01'],
  },
};

const BASE_URL = 'http://localhost:5249/LopHocPhan';

// ID hợp lệ của HocPhan, HocKi, GiangVien (cần có sẵn trong CSDL)
const VALID_HOC_PHAN_ID = 'e45a4a03-3b6d-46bc-af40-6c268bc44d75'; //KT_453
const VALID_HOC_KI_ID = '7ec49d4e-3758-4053-9c79-c156eaccb754';
const VALID_GIANG_VIEN_ID = '6196ce2a-e452-454d-bed6-7f0820a6cded'; //PU_KT_25

export default function () {
  // 1. GET danh sách lớp học phần
  const getRes = http.get(BASE_URL);
  check(getRes, {
    'GET /LopHocPhan trả về 200': (r) => r.status === 200,
  });

  // 2. POST tạo lớp học phần mới
  const payload = JSON.stringify({
    hocPhanId: VALID_HOC_PHAN_ID,
    hocKiId: VALID_HOC_KI_ID,
    soLuongSinhVien: Math.floor(Math.random() * 100),
    giangVienId: VALID_GIANG_VIEN_ID
  });
  const headers = { 'Content-Type': 'application/json' };
  const postRes = http.post(`${BASE_URL}/them-hoc-phan`, payload, { headers });

  check(postRes, {
    'POST /LopHocPhan/them-hoc-phan trả về 200': (r) => r.status === 200,
  });

  if (postRes.status !== 200) {
    console.warn(`❌ POST thất bại: ${postRes.status}, body: ${postRes.body}`);
    return;
  }

  const createdLop = postRes.json();
  const lopId = createdLop.id;

  // 3. PUT sửa thông tin lớp học phần
  const putPayload = JSON.stringify({
    id: lopId,
    hocPhanId: VALID_HOC_PHAN_ID,
    hocKiId: VALID_HOC_KI_ID,
    soLuongSinhVien: 123,
    giangVienId: VALID_GIANG_VIEN_ID
  });
  const putRes = http.put(`${BASE_URL}/sua-thong-tin`, putPayload, { headers });
  check(putRes, {
    'PUT /sua-thong-tin trả về 200': (r) => r.status === 200,
  });

  // 4. POST phân công giảng viên
  const assignRes = http.post(`${BASE_URL}/phan-cong-giang-vien`, JSON.stringify({
    lopHocPhanId: lopId,
    giangVienId: VALID_GIANG_VIEN_ID
  }), { headers });
  check(assignRes, {
    'POST /phan-cong-giang-vien trả về 200': (r) => r.status === 200,
  });

  // 5. DELETE lớp học phần vừa tạo
  const delRes = http.del(`${BASE_URL}/xoa/${lopId}`);
  check(delRes, {
    'DELETE /xoa/:id trả về 200': (r) => r.status === 200,
  });

  sleep(1);
}
