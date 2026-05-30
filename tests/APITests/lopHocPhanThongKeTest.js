// lopHocPhanThongKeTest.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 50,
  duration: '20s',
  thresholds: {
    http_req_duration: ['p(95)<1000'],
    http_req_failed: ['rate<0.01'],
  },
};

const BASE = 'http://localhost:5249/LopHocPhanThongKe';

export default function () {
  // 1. GET danh sách năm học kỳ
  const namHocRes = http.get(`${BASE}/nam-hoc-ki`);
  check(namHocRes, {
    'GET /nam-hoc-ki trả về 200': (r) => r.status === 200,
  });

  // 2. Thống kê theo khoa
  const khoaRes = http.get(`${BASE}/thong-ke-khoa`);
  check(khoaRes, {
    'GET /thong-ke-khoa trả về 200': (r) => r.status === 200,
  });

  // 3. Thống kê theo học phần từ một ngày cụ thể
  const thongKeHocPhanRes = http.get(`${BASE}/thong-ke-hoc-phan`, {
    params: {
      dateTime: '01/01/2020', // format dd/MM/yyyy (nếu backend sử dụng văn hóa en-US thì cần đổi)
    },
  });
  check(thongKeHocPhanRes, {
    'GET /thong-ke-hoc-phan trả về 200': (r) => r.status === 200,
  });

  // 4. Lấy danh sách học kỳ từ API để test thống kê theo học kỳ
  const hocKiList = JSON.parse(namHocRes.body);
  if (hocKiList.length > 0) {
    const hocKiId = hocKiList[0].Id;
    const hocKiRes = http.get(`${BASE}/thong-ke-hoc-ki`, {
      params: { hocKi: hocKiId },
    });
    check(hocKiRes, {
      'GET /thong-ke-hoc-ki trả về 200': (r) => r.status === 200,
    });
  } else {
    console.warn('⚠️ Không có dữ liệu học kỳ để test /thong-ke-hoc-ki');
  }

  sleep(1);
}