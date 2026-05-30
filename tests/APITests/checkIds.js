import http from 'k6/http';

export default function () {
  console.log('== BangCap ==');
  console.log(http.get('http://localhost:5249/BangCap').body);

  console.log('== Khoa ==');
  console.log(http.get('http://localhost:5249/Khoa').body);

  console.log('== ChucVu ==');
  console.log(http.get('http://localhost:5249/ChucVu').body);
}
