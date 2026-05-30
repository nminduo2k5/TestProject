import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 50, // số lượng người dùng ảo đồng thời
  duration: '15s',
  thresholds: {
    http_req_duration: ['p(95)<1000'], // 95% request < 2s
    http_req_failed: ['rate<0.01'],    // < 1% request bị lỗi
  },
};

export default function () {
  // 1. Gửi GET để lấy danh sách học kỳ
  const getRes = http.get('http://localhost:5249/HocKi');
  check(getRes, {
    'GET /HocKi trả về 200': (r) => r.status === 200,
    'GET có dữ liệu': (r) => r.body && r.body.length > 10,
  });

  // 2. Gửi POST để tạo học kỳ mới
  const payload = JSON.stringify({
    tenKi: `Học kỳ K6-${Math.floor(Math.random() * 1000)}`,
    thoiGianBatDau: '2026-01-01T00:00:00',
    thoiGianKetThuc: '2026-06-01T00:00:00',
  });

  const headers = { 'Content-Type': 'application/json' };
  const postRes = http.post('http://localhost:5249/HocKi', payload, { headers });

  check(postRes, {
    'POST /HocKi trả về 200 hoặc 201': (r) => r.status === 200 || r.status === 201,
    'POST trả về ID mới': (r) => r.body.includes('id'),
  });

  sleep(1); // nghỉ 1s mô phỏng người dùng thật
}
