import http from 'k6/http';
import { check, group } from 'k6';
import { Trend } from 'k6/metrics';

// Thống kê thời gian phản hồi
const myTrend = new Trend('response_time');

export const options = {
  vus: 5,
  duration: '5s',
};

export default function () {
  group('GET /thong-ke-giao-vien', () => {
    const res = http.get('http://localhost:5249/thong-ke-giao-vien');

    // Ghi lại thời gian phản hồi
    myTrend.add(res.timings.duration);

    check(res, {
      'status là 200': (r) => r.status === 200,
      'có trả về JSON': (r) =>
        r.headers['Content-Type'] &&
        r.headers['Content-Type'].indexOf('application/json') !== -1,
      'có chứa trường BangCap': (r) => {
        try {
          return r.json().hasOwnProperty('BangCap');
        } catch (e) {
          return false;
        }
      },
      'có chứa trường GioiTinh': (r) => {
        try {
          return r.json().hasOwnProperty('GioiTinh');
        } catch (e) {
          return false;
        }
      },
      'có chứa trường KhoaList': (r) => {
        try {
          return r.json().hasOwnProperty('KhoaList');
        } catch (e) {
          return false;
        }
      },
      'có chứa trường BangCapList': (r) => {
        try {
          return r.json().hasOwnProperty('BangCapList');
        } catch (e) {
          return false;
        }
      },
    });
  });
}
