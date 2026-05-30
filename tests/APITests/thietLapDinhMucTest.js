import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 5,
  duration: '10s',
};

const BASE_URL = 'http://localhost:5249/DinhMuc';

export default function () {
  // 1. GET tất cả định mức
  const getRes = http.get(BASE_URL);
  check(getRes, {
    'GET /DinhMuc trả về 200': (r) => r.status === 200,
  });

  // 2. POST tạo định mức mới
  const payload = JSON.stringify({
    soTien: Math.floor(Math.random() * 1000000 + 100000),
    lyDo: `Thiết lập tự động lúc ${new Date().toISOString()}`
  });

  const headers = { 'Content-Type': 'application/json' };
  const postRes = http.post(BASE_URL, payload, { headers });

  check(postRes, {
    'POST /DinhMuc trả về 200': (r) => r.status === 200,
    'POST trả về object có SoTien': (r) => JSON.parse(r.body).soTien > 0,
  });

  sleep(1);
}
