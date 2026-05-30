import http from 'k6/http';
import { check, group } from 'k6';

const BASE_URL = 'http://localhost:5249';

export default function () {
  group('Kiểm thử API thống kê giáo viên', () => {
    const res = http.get(`${BASE_URL}/thong-ke-giao-vien`);

    check(res, {
      'Trạng thái trả về 200': (r) => r.status === 200,
      'Content-Type là application/json': (r) => r.headers['Content-Type'] && r.headers['Content-Type'].includes('application/json'),
    });

    const body = res.json();

    // Kiểm tra có đầy đủ các trường chính
    check(body, {
      'Trả về BangCap': (r) => Array.isArray(r.BangCap),
      'Trả về GioiTinh': (r) => Array.isArray(r.GioiTinh),
      'Trả về KhoaList': (r) => Array.isArray(r.KhoaList),
      'Trả về BangCapList': (r) => Array.isArray(r.BangCapList),
    });

    // Kiểm tra cấu trúc dữ liệu trong BangCap
    if (Array.isArray(body.BangCap)) {
      check(body.BangCap[0], {
        'BangCap có MaKhoa': (item) => item && item.hasOwnProperty('MaKhoa'),
        'BangCap có TenKhoa': (item) => item && item.hasOwnProperty('TenKhoa'),
        'BangCap có MaBangCap': (item) => item && item.hasOwnProperty('MaBangCap'),
        'BangCap có TenBangCap': (item) => item && item.hasOwnProperty('TenBangCap'),
        'BangCap có SoGiangVien': (item) => item && item.hasOwnProperty('SoGiangVien'),
      });
    }

    // Kiểm tra cấu trúc dữ liệu trong GioiTinh
    if (Array.isArray(body.GioiTinh)) {
      check(body.GioiTinh[0], {
        'GioiTinh có MaKhoa': (item) => item && item.hasOwnProperty('MaKhoa'),
        'GioiTinh có TenKhoa': (item) => item && item.hasOwnProperty('TenKhoa'),
        'GioiTinh có GioiTinh': (item) => item && item.hasOwnProperty('GioiTinh'),
        'GioiTinh có GioiTinhText': (item) => item && item.hasOwnProperty('GioiTinhText'),
        'GioiTinh có SoGiangVien': (item) => item && item.hasOwnProperty('SoGiangVien'),
      });
    }

    // Kiểm tra dữ liệu KhoaList
    if (Array.isArray(body.KhoaList)) {
      check(body.KhoaList[0], {
        'KhoaList có MaKhoa': (item) => item && item.hasOwnProperty('MaKhoa'),
        'KhoaList có TenKhoa': (item) => item && item.hasOwnProperty('TenKhoa'),
        'KhoaList có TenVietTat': (item) => item && item.hasOwnProperty('TenVietTat'),
      });
    }

    // Kiểm tra dữ liệu BangCapList
    if (Array.isArray(body.BangCapList)) {
      check(body.BangCapList[0], {
        'BangCapList có MaBangCap': (item) => item && item.hasOwnProperty('MaBangCap'),
        'BangCapList có TenBangCap': (item) => item && item.hasOwnProperty('TenBangCap'),
        'BangCapList có TenVietTat': (item) => item && item.hasOwnProperty('TenVietTat'),
      });
    }
  });
}
