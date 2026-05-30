import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 5,
  duration: '15s',
};

const BASE_URL = 'http://localhost:5249/HeSoBangCap';
const CURRENT_YEAR = new Date().getFullYear();
const EXISTING_MA_BANG_CAP = '5e50cf12-3ae6-4515-8ffa-3a1b628beead'; // ← THAY bằng ID hợp lệ có thật trong DB

export default function () {
  // 1. GET tất cả hệ số bằng cấp
  const getAll = http.get(BASE_URL);
  check(getAll, {
    'GET /HeSoBangCap trả về 200': (r) => r.status === 200,
  });

  // 2. GET theo năm → auto insert nếu chưa có
  const getByYear = http.get(`${BASE_URL}/${CURRENT_YEAR}`);
  check(getByYear, {
    [`GET /HeSoBangCap/${CURRENT_YEAR} trả về 200`]: (r) => r.status === 200,
  });

  // 3. POST thêm hệ số mới (hoặc update nếu đã tồn tại)
  const payload = JSON.stringify({
    maBangCap: EXISTING_MA_BANG_CAP,
    heSo: Math.round(Math.random() * 10 * 100) / 100, // ví dụ 3.45
    nam: CURRENT_YEAR
  });

  const headers = { 'Content-Type': 'application/json' };
  const postRes = http.post(BASE_URL, payload, { headers });

  check(postRes, {
    'POST /HeSoBangCap trả về 200': (r) => r.status === 200,
  });

  sleep(1);
}
