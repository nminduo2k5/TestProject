import { faChalkboardTeacher, faMoneyBillWave, faUserTie } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Button, Card, Col, Divider, Modal, Row, Select, Statistic, Table, Tag } from 'antd';
import { useEffect, useMemo, useState } from 'react';
import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';


import { GetHocKyList } from '@/api/hocKiApi';
import { GetKhoaList } from '@/api/khoaApi';
import { GetNamHocList } from '@/api/lhpThongKeApi';
import { GetDinhMuc, GetHeSoLopHocPhan, TinhTienDay } from '@/api/tinhTienDay';
import { faFileExcel } from '@fortawesome/free-regular-svg-icons';

function LayHeSoDinhMucSinhVien(danhSachHeSoLop, soHocSinhToiThieu, namHoc) {
  const result = danhSachHeSoLop.filter(i => i.soHocSinhToiThieu <= soHocSinhToiThieu && i.namHoc <= namHoc)
  return result.length > 0 ? result[result.length - 1].heSo : 1;
}

// function LayDinhMuc(danhSachDinhMuc, namHoc) {
//   const result = danhSachDinhMuc.filter(i => new Date(i.ngayCapNhat).getFullYear() <= namHoc)
//   return (result.length > 0 ? result[result.length - 1] : danhSachDinhMuc[0])?.soTien || 1;
// }
function LayDinhMuc(danhSachDinhMuc, namHoc) {
  // Tìm bản ghi có ngày cập nhật gần nhất nhưng không lớn hơn ngày 1/1/(namHoc + 1)
  const limitDate = new Date(`${namHoc + 1}-01-01`);
  const result = danhSachDinhMuc
    .filter(i => new Date(i.ngayCapNhat) < limitDate)
    .sort((a, b) => new Date(a.ngayCapNhat) - new Date(b.ngayCapNhat));

  return (result.length > 0 ? result[result.length - 1] : danhSachDinhMuc[0])?.soTien || 1;
}
function GetYear(str) {
  return new Date(str).getFullYear();
}

const exportToExcel = (data, fileName = 'export.xlsx') => {
  // Chuyển dữ liệu thành worksheet
  const worksheet = XLSX.utils.json_to_sheet(data);

  const colWidths = Object.keys(data[0]).map(key => {
    const maxLength = Math.max(
      key.length,
      ...data.map(row => (row[key] ? row[key].toString().length : 0))
    );
    return { wch: maxLength + 2 }; // +2 cho thoáng
  });

  worksheet['!cols'] = colWidths;


  // Tạo workbook
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');

  // Ghi file vào blob
  const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
  const dataBlob = new Blob([excelBuffer], { type: 'application/octet-stream' });

  // Lưu file
  saveAs(dataBlob, fileName);
};

function TienDayGiangVien() {
  // modal
  const [detailModalVisible, setDetailModalVisible] = useState(false);
  const [selectedTeacher, setSelectedTeacher] = useState(null);

  // console.log(selectedTeacher)

  // data
  const [tienDayData, setTienDayData] = useState([])
  const [khoa, setKhoa] = useState([])
  const [kyHoc, setKyHoc] = useState([])
  const [namHoc, setNamHoc] = useState([])
  const [heSoLopHocPhan, setHeSoLopHocPhan] = useState([])
  const [dinhMucSoTietChuan, setDinhMucSoTienChuan] = useState([])
  // console.log(kyHoc)
  // form
  const [filterForm, setFilterForm] = useState({ khoa: 'all', kyHoc: null, namHoc: null })
  /*
{
    "id": "39c566e4-7dba-48d9-a5b9-60eef656590a",
    "maGiangVien": "PU_HH_973",
    "tenGiangVien": "kCWJ",
    "khoaId": "64cb87b4-0e25-4092-8daf-67da44ec3297",
    "maKhoa": "FAC_HH",
    "tenKhoa": "Khoa Hóa học",
    "maBangCap": "DEG_1",
    "tenBangCap": "Giáo sư",
    "maLop": "FAC_CK_638852787425150195-1529",
    "tenLop": "ec0-c524-4922-b (N1529)",
    "soLuongSinhVien": 199,
    "maHocKi": "7f24ebd1-8a2d-4ae2-a454-a8eadb2fe169",
    "thoiGianBatDau": "1950-08-01T22:37:41.671Z",
    "thoiGianKetThuc": "1951-02-01T22:37:41.671Z",
    "heSoBangCap": 1,
    "hocPhanId": "b5937ca9-84be-40b1-ad55-617644f8a36c",
    "maHocPhan": "FAC_CK_638852787425150195",
    "tenHocPhan": "ec0-c524-4922-b",
    "soTiet": 293,
    "soTinChi": 3,
    "heSoHocPhan": 8.740433692932129
}
  */
  // console.log(tienDayData)
  console.log(selectedTeacher)
  const tinhTienTableData = useMemo(() => {
    const result = {}

    for (const item of tienDayData) {
      const namHoc = new Date(item.thoiGianBatDau).getFullYear()
      if (filterForm.khoa != 'all' && item.khoaId != filterForm.khoa) continue
      if (namHoc != filterForm?.namHoc) continue
      if (filterForm.kyHoc && item.maHocKi != filterForm.kyHoc) continue

      if (result[item.id] != null) {
        result[item.id].soLop += 1;
        continue
      }

      result[item.id] = {
        id: item.id,
        khoaId: item.khoaId,
        maKhoa: item.maKhoa,
        tenKhoa: item.tenKhoa,
        maHocKi: item.maHocKi,
        tenHocKy: item.tenHoc,
        namHoc,
        soLop: 1,
        maGiangVien: item.maGiangVien,
        tenGiangVien: item.tenGiangVien,
        maBangCap: item.maBangCap,
        tenBangCap: item.tenBangCap,
        tienDay: item.soTiet * (
          item.heSoHocPhan
          + LayHeSoDinhMucSinhVien(heSoLopHocPhan, item.soLuongSinhVien, namHoc)
        ) * item.heSoBangCap * LayDinhMuc(dinhMucSoTietChuan, namHoc)
      }
    }
    return Object.values(result)
  }, [dinhMucSoTietChuan, filterForm, heSoLopHocPhan, tienDayData])
  // filterForm

  useEffect(function () {
    // fetch data
    GetKhoaList().then(setKhoa)
    GetNamHocList().then(data => {
      const sortedData = data.sort((a, b) => b.nam - a.nam);
      setNamHoc(sortedData)
      setFilterForm(e => ({ ...e, namHoc: sortedData[0]?.nam || new Date().getFullYear() }))
    })
    GetHocKyList().then(data => {
      setKyHoc(data)
      setFilterForm(e => ({ ...e, kyHoc: data[0]?.id || null }))
    })
    TinhTienDay().then(setTienDayData)
    GetDinhMuc().then(setDinhMucSoTienChuan)
    GetHeSoLopHocPhan().then(setHeSoLopHocPhan)
  }, [])

  const tienDayColumns = [
    { title: 'Mã GV', dataIndex: 'maGiangVien', key: 'maGiangVien', },
    { title: 'Tên giáo viên', dataIndex: 'tenGiangVien', key: 'tenGiangVien', },
    {
      title: 'Bằng cấp', dataIndex: 'tenBangCap', key: 'tenBangCap',
      render: value => <Tag color="blue">{value}</Tag>
    },
    { title: 'Khoa', dataIndex: 'tenKhoa', key: 'tenKhoa', },
    {
      title: 'Số lớp', dataIndex: 'soLop', key: 'soLop',
      render: value => <Tag color="orange">{value} lớp</Tag>
    },
    {
      title: 'Tổng tiền (VNĐ)', dataIndex: 'tienDay', key: 'tienDay',
      render: value => <span style={{ fontWeight: 'bold', color: '#1890ff' }}>{value?.toLocaleString('vi-VN')}</span>

    },
    {
      title: 'Thao tác', key: 'action',
      render: (_, record) => (
        <Button data-testid="btn-chi-tiet" type="link"
          onClick={() => {
            setSelectedTeacher({
              ...record,
              chiTiet: tienDayData
                ?.filter(i => i.id == record.id
                  && (filterForm.namHoc == 'all' || new Date(i.thoiGianBatDau).getFullYear() == filterForm.namHoc)
                  && (filterForm.kyHoc == null || i.maHocKi == filterForm.kyHoc)
                  && (filterForm.khoa == 'all' || i.khoaId == filterForm.khoa))
                .map(i => ({
                  ...i,
                  tienDay: i.soTiet * (
                    i.heSoHocPhan
                    + LayHeSoDinhMucSinhVien(heSoLopHocPhan, i.soLuongSinhVien, GetYear(i.thoiGianBatDau))
                  ) * i.heSoBangCap * LayDinhMuc(dinhMucSoTietChuan, GetYear(i.thoiGianBatDau))
                }))
            });

            setDetailModalVisible(true);
          }}>Chi tiết</Button>
      ),
    },
  ];
  const chiTietColumns = [
    { title: 'STT', render: (_, record, index) => index + 1, },
    { title: 'Mã lớp', dataIndex: 'maLop', key: 'maLop', },
    { title: 'Tên học phần', dataIndex: 'tenHocPhan', key: 'tenHocPhan', },
    { title: 'Số tiết', dataIndex: 'soTiet', key: 'soTiet', },
    { title: 'Số SV', dataIndex: 'soLuongSinhVien', key: 'soLuongSinhVien', },
    { title: 'Hệ số HP', dataIndex: 'heSoHocPhan', key: 'heSoHocPhan', render: (value) => value?.toFixed(2) },
    { title: 'Tiền dạy (VNĐ)', dataIndex: 'tienDay', key: 'tienDay', render: (value) => value?.toLocaleString('vi-VN') }
  ];

  return (
    <>
      <div className='p-5'>
        <Card title="Bộ lọc tính tiền dạy">
          <Row gutter={16}>
            <Col span={6}>
              <Select placeholder="Chọn khoa" style={{ width: '100%' }}
                value={filterForm.khoa}
                onChange={(value) => setFilterForm({ ...filterForm, khoa: value })}
                options={[
                  { value: "all", label: "Toàn trường" },
                  ...khoa.map(i => ({ value: i.id, label: i.tenKhoa }))
                ]} />
            </Col>
            <Col span={6}>
              <Select placeholder="Năm học" style={{ width: '100%' }}
                value={filterForm.namHoc}
                onChange={(value) => {
                  setFilterForm({
                    ...filterForm,
                    namHoc: value,
                    kyHoc: kyHoc.find(i => GetYear(i.thoiGianBatDau) == value)?.id || null
                  })
                }}
                options={[
                  ...namHoc.map(i => ({ value: i.nam, label: `${i.nam} - ${i.nam + 1}` }))
                ]} />
            </Col>
            <Col span={6}>
              <Select placeholder="Kì học" style={{ width: '100%' }} disabled={filterForm.namHoc === 'all'}
                value={filterForm.kyHoc}
                onChange={(value) => {
                  setFilterForm({ ...filterForm, kyHoc: value })
                }}
                options={[
                  ...kyHoc
                    .filter(i => GetYear(i.thoiGianBatDau) == filterForm.namHoc)
                    .map(i => ({ value: i.id, label: i.tenKi }))
                ]} />
            </Col>
            <Col span={3}>
              <Button variant='solid' style={{ width: '100%', backgroundColor: '#19A10A', color: 'white' }}
                icon={<FontAwesomeIcon icon={faFileExcel} />}
                onClick={() => {
                  const mapping = {

                    "id": "Mã giảng viên",
                    // "khoaId": "Mã khoa",
                    "maKhoa": "Mã khoa",
                    "tenKhoa": "Tên khoa",
                    // "maHocKi": "ddd2503b-df17-4a92-a280-cbdc3a0bffa0",
                    "namHoc": "Năm học",
                    "soLop": "Số lớp dạy",
                    "maGiangVien": "Mã giảng viên",
                    "tenGiangVien": "Họ tên giảng viên",
                    "maBangCap": "Mã bằng cấp",
                    "tenBangCap": "Tên bằng cấp",
                    "tienDay": "Tiền dạy"

                  }
                  // console.log(tinhTienTableData
                  //   .map(i => Object.fromEntries(Object
                  //     .entries(i)
                  //     .map(([key, value]) => [mapping[key], value])
                  //     .filter(([key]) => key)
                  //   )))
                  exportToExcel(
                    tinhTienTableData
                      .map(i => Object.fromEntries(Object
                        .entries(i)
                        .map(([key, value]) => [mapping[key], value])
                        .filter(([key]) => key)
                      )),
                    'tinh-tien-day.xlsx')
                }}>
                Xuất file excel
              </Button>
            </Col>
          </Row>
        </Card>

        <Card title="Kết quả tính tiền dạy" style={{ marginTop: '16px' }}>
          <Row gutter={16} style={{ marginBottom: '16px' }}>
            <Col span={8}>
              <Statistic prefix={<FontAwesomeIcon icon={faUserTie} />}
                title="Tổng số giáo viên"
                value={tinhTienTableData.length} />
            </Col>
            <Col span={8}>
              <Statistic prefix={<FontAwesomeIcon icon={faChalkboardTeacher} />}
                title="Tổng số lớp"
                value={tinhTienTableData.reduce((prev, curr) => prev + curr.soLop, 0)} />
            </Col>
            <Col span={8}>
              <Statistic prefix={<FontAwesomeIcon icon={faMoneyBillWave} />}
                formatter={(value) => value?.toLocaleString('vi-VN') + ' VNĐ'}
                title="Tổng tiền chi trả"
                value={tinhTienTableData.reduce((prev, curr) => prev + curr.tienDay, 0)} />
            </Col>
          </Row>

          <Table columns={tienDayColumns} dataSource={tinhTienTableData} pagination={{ pageSize: 10 }} size="middle" />
        </Card>
      </div>

      {/* Modal chi tiết tính tiền */}
      <Modal
        title={<p className='font-bold uppercase text-blue-900 text-xl'>Chi tiết tiền dạy - {selectedTeacher?.tenGiangVien}</p>}
        width={900}
        open={detailModalVisible}
        onCancel={() => {
          setDetailModalVisible(false)
          setSelectedTeacher(null)
        }}
        footer={[
          <Button key="close" variant='solid' color='orange'
            onClick={() => setDetailModalVisible(false)}>
            Đóng
          </Button>
        ]}>
        {selectedTeacher && (
          <>
            <Row className='bg-lime-100 border-lime-500 border my-10 p-5 rounded-xl' gutter={16} style={{ margin: '16px 0' }}>
              <Col span={12}>
                {/* <Card size="small"> */}
                <Statistic title={<p className='font-bold text-black'>Bằng cấp</p>}
                  value={selectedTeacher.tenBangCap}
                  valueStyle={{ fontSize: '16px' }} />
                {/* </Card> */}
              </Col>
              <Col span={12}>
                {/* <Card size="small"> */}
                <Statistic title={<p className='font-bold text-black'>Tổng tiền</p>}
                  value={selectedTeacher.chiTiet.reduce((prev, curr) => prev + curr.tienDay, 0)}
                  formatter={(value) => value?.toLocaleString('vi-VN') + ' VNĐ'}
                  valueStyle={{ color: 'black', fontSize: '16px' }} />
                {/* </Card> */}
              </Col>
            </Row>

            <p className='text-center font-bold text-blue-900 text-lg'>Chi tiết các lớp dạy:</p>

            <Table columns={chiTietColumns} dataSource={selectedTeacher.chiTiet} size="small"
              pagination={{
                pageSize: 6,
                showSizeChanger: true,
                showQuickJumper: true,
                showTotal: (total, range) => `${range[0]}-${range[1]} của ${total} lớp học phần`
              }} />

            <div className='mt-4 p-3 rounded-lg bg-gray-100' >
              <h4>Công thức tính:</h4>
              <p className='font-semibold'>Tiền dạy mỗi lớp = Số tiết quy đổi × Hệ số giáo viên × Tiền dạy một tiết</p>
              <p className='font-semibold'>Số tiết quy đổi = Số tiết thực tế × (Hệ số học phần + Hệ số lớp)</p>
            </div>
          </>
        )}
      </Modal >
    </>
  )
}

export default TienDayGiangVien;