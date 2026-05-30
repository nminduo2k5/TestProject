import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 50, // 50 người dùng ảo đồng thời
  duration: '15s', // test trong 15 giây
  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% request phải dưới 1s
    http_req_failed: ['rate<0.01'],     // Tỷ lệ thất bại dưới 1%
  },
};

export default function () {
  const res = http.get('http://localhost:5249/TinhTienDay');

  check(res, {
    'Trạng thái là 200': (r) => r.status === 200,
    'Thời gian phản hồi < 1s': (r) => r.timings.duration < 1000,
    'Có dữ liệu trả về': (r) => r.body && r.body.length > 10,
  });

  sleep(1); // nghỉ 1s giữa các lần gọi để mô phỏng thực tế
}
