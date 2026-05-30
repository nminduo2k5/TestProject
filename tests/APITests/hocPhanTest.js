import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 50,
  duration: '20s',
  thresholds: {
    http_req_duration: ['p(95)<2000'],
    http_req_failed: ['rate<0.02'],
  },
};

const BASE_URL = 'http://localhost:5249/HocPhan';

// 👇 Thay bằng ID thật của Khoa (đã tồn tại)
const EXISTING_KHOA_ID = 'e93691e4-7b24-488b-8ccf-7668d3aae9ed';

export default function () {
  // 1. GET tất cả học phần
  const getAllRes = http.get(BASE_URL);
  check(getAllRes, {
    'GET /HocPhan trả về 200': (r) => r.status === 200,
  });

  // 2. POST tạo học phần mới
  const maHocPhan = `HP${__VU}_${__ITER}_${Math.floor(Math.random() * 1000)}`;
  const payload = JSON.stringify({
    maHocPhan,
    tenHocPhan: `Học phần K6 ${maHocPhan}`,
    heSoHocPhan: 2,
    soTinChi: 3,
    soTiet: 45,
    khoaId: EXISTING_KHOA_ID,
  });
  const headers = { 'Content-Type': 'application/json' };
  const postRes = http.post(BASE_URL, payload, { headers });

  check(postRes, {
    'POST /HocPhan trả về 201': (r) => r.status === 201,
  });

  if (postRes.status !== 201) {
    console.warn(`❌ POST thất bại: ${postRes.status}, body: ${postRes.body}`);
    return;
  }

  // 🔁 Chờ DB cập nhật rồi mới truy vấn lại
  sleep(0.5);

  // 3. GET để tìm lại học phần vừa tạo
  const getAfterPost = http.get(BASE_URL);
  let createdItem;
  try {
    const hpList = getAfterPost.json();
    createdItem = hpList.find(hp => hp.MaHocPhan === maHocPhan);
  } catch (err) {
    console.warn(`❌ Lỗi JSON parse từ GET sau POST: ${getAfterPost.body}`);
    return;
  }

  if (!createdItem) {
    console.warn(`⚠️ Không tìm thấy học phần vừa tạo với mã: ${maHocPhan}`);
    return;
  }

  const id = createdItem.Id;

  // 4. PUT sửa học phần
  const putPayload = JSON.stringify({
    tenHocPhan: `Học phần sửa ${maHocPhan}`,
    heSoHocPhan: 3,
    soTinChi: 4,
    soTiet: 60,
    khoaId: EXISTING_KHOA_ID,
  });
  const putRes = http.put(`${BASE_URL}/sua-hoc-phan/${id}`, putPayload, { headers });

  check(putRes, {
    'PUT /HocPhan/sua-hoc-phan trả về 200': (r) => r.status === 200,
  });

  if (putRes.status !== 200) {
    console.warn(`❌ PUT thất bại: ${putRes.status}, body: ${putRes.body}`);
    return;
  }

  // 5. DELETE học phần
  const delRes = http.del(`${BASE_URL}?id=${id}`);
  check(delRes, {
    'DELETE /HocPhan?id= trả về 200': (r) => r.status === 200,
  });

  if (delRes.status !== 200) {
    console.warn(`❌ DELETE thất bại: ${delRes.status}, body: ${delRes.body}`);
  }

  sleep(1);
}
