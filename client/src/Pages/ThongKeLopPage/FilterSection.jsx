import { BarChartOutlined, FileExcelOutlined } from '@ant-design/icons';
import { Button, Card, Col, message, Row, Select, Space } from 'antd';
import { useState } from 'react';
import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';

import { useData } from './context';
import { GetThongKeLopHocPhanTheoHocKi, GetThongKeLopHocPhanTheoHocPhan, GetThongKeLopHocPhanTheoKhoa } from '@/api/lhpThongKeApi';

const exportToExcel = (data, fileName = 'thong-ke-lop-hoc-phan.xlsx') => {
  if (!data || data.length === 0) {
    message.warning("Không có dữ liệu để xuất báo cáo!");
    return;
  }

  const exportData = data.map(item => ({
    "Mã học phần": item.maHocPhan,
    "Tên học phần": item.tenHocPhan,
    "Số lớp mở": item.soLopHocPhan,
    "Tổng sinh viên": item.tongSinhVien,
    "SV trung bình/lớp": (item.trungBinhSinhVienLop ?? 0).toFixed(0),
    "Khoa": item.tenKhoa
  }));

  const worksheet = XLSX.utils.json_to_sheet(exportData);
  const colWidths = Object.keys(exportData[0]).map(key => ({
    wch: Math.max(key.length, ...exportData.map(row => (row[key] ? row[key].toString().length : 0))) + 4
  }));
  worksheet['!cols'] = colWidths;

  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, 'ThongKeLopHocPhan');
  const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
  const dataBlob = new Blob([excelBuffer], { type: 'application/octet-stream' });
  saveAs(dataBlob, fileName);
  message.success("Đã xuất file báo cáo Excel thành công!");
};

function FilterSection() {
  const [{
    selectedKhoa, selectedKy, selectedNam,
    khoaData, namHocData, hocKiData, thongKeHocPhan
  }, dispatch] = useData();

  const [loading, setLoading] = useState(false);

  const handleThongKe = async () => {
    setLoading(true);
    try {
      let data = [];
      if (selectedKy && selectedKy !== 'all') {
        data = await GetThongKeLopHocPhanTheoHocKi(selectedKy);
      } else if (selectedNam && selectedNam !== 'all') {
        data = await GetThongKeLopHocPhanTheoHocPhan(new Date(selectedNam, 0, 1));
      } else {
        data = await GetThongKeLopHocPhanTheoHocPhan();
      }

      dispatch({
        type: 'updateData',
        payload: { key: 'thongKeHocPhan', data }
      });
      message.success("Đã cập nhật dữ liệu thống kê!");
    } catch (err) {
      console.error(err);
      message.error("Có lỗi xảy ra khi tải dữ liệu thống kê!");
    } finally {
      setLoading(false);
    }
  };

  const filteredData = (thongKeHocPhan || []).filter(item => {
    return (selectedKhoa === 'all' || !selectedKhoa || item.khoaId === selectedKhoa);
  });

  return (
    <Card style={{ marginBottom: '12px', marginTop: "12px" }}>
      <Row gutter={16}>
        <Col span={6}>
          <div style={{ marginBottom: '8px', fontWeight: 'bold' }}>Khoa:</div>
          <Select
            placeholder="Chọn khoa" style={{ width: '100%' }} allowClear
            value={selectedKhoa || undefined}
            onChange={a => dispatch([{ type: 'updateSelectedKhoa', payload: a || 'all' }])}
            options={[
              { value: 'all', label: 'Tất cả khoa' },
              ...(khoaData?.map(k => ({ value: k.id, label: k.tenKhoa })) || [])
            ]} />
        </Col>
        <Col span={6}>
          <div style={{ marginBottom: '8px', fontWeight: 'bold' }}>Năm học:</div>
          <Select
            placeholder="Chọn năm học"
            style={{ width: '100%' }}
            value={selectedNam || undefined}
            onChange={async a => {
              const val = a || 'all';
              let data = [];
              if (val !== 'all') {
                data = await GetThongKeLopHocPhanTheoHocPhan(new Date(val, 0, 1));
              } else {
                data = await GetThongKeLopHocPhanTheoHocPhan();
              }
              dispatch([
                { type: 'updateData', payload: { key: 'thongKeHocPhan', data } },
                { type: 'updateSelectedNam', payload: val },
                { type: 'updateSelectedKy', payload: 'all' }
              ]);
            }}
            allowClear
            options={[
              { value: 'all', label: 'Tất cả năm học' },
              ...(namHocData?.map(nam => ({ value: nam.nam, label: `${nam.nam}-${nam.nam + 1}` })) || [])
            ]} />
        </Col>
        <Col span={6}>
          <div style={{ marginBottom: '8px', fontWeight: 'bold' }}>Kỳ học:</div>
          <Select
            placeholder="Chọn kỳ học"
            style={{ width: '100%' }}
            allowClear
            disabled={selectedNam === 'all' || !selectedNam}
            value={selectedKy || undefined}
            onChange={async (a) => {
              const val = a || 'all';
              let data = [];
              if (val !== 'all') {
                data = await GetThongKeLopHocPhanTheoHocKi(val);
              } else if (selectedNam !== 'all') {
                data = await GetThongKeLopHocPhanTheoHocPhan(new Date(selectedNam, 0, 1));
              } else {
                data = await GetThongKeLopHocPhanTheoHocPhan();
              }
              dispatch([
                { type: 'updateData', payload: { key: 'thongKeHocPhan', data } },
                { type: 'updateSelectedKy', payload: val }
              ]);
            }}
            options={[
              { value: 'all', label: 'Tất cả kỳ học' },
              ...(hocKiData || [])
                .filter(ky => new Date(ky.thoiGianBatDau).getFullYear() == selectedNam)
                .map(ky => ({ value: ky.id, label: ky.tenKi }))
            ]} />
        </Col>
        <Col span={6}>
          <div style={{ marginBottom: '8px' }}>&nbsp;</div>
          <Space>
            <Button
              type="primary"
              icon={<BarChartOutlined />}
              loading={loading}
              onClick={handleThongKe}>
              Thống kê
            </Button>
            <Button
              type='primary'
              icon={<FileExcelOutlined />}
              style={{ backgroundColor: '#19A10A', borderColor: '#19A10A' }}
              onClick={() => exportToExcel(filteredData, `thong-ke-lop-hoc-phan-${selectedNam || 'all'}.xlsx`)}>
              Xuất báo cáo
            </Button>
          </Space>
        </Col>
      </Row>
    </Card>
  );
}

export default FilterSection;