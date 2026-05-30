import { AccountBookOutlined, BookOutlined, TeamOutlined } from '@ant-design/icons';
import { Card, Col, Row, Statistic } from 'antd';

import { useData } from './context';

function OverallStats() {
  const [{
    selectedKhoa, selectedKy, thongKeHocPhan
  }, dispatch] = useData()

  const filteredData = thongKeHocPhan.filter(item => selectedKhoa == 'all' || item.khoaId === selectedKhoa);

  // Tính toán thống kê tổng
  const tongSoLop = filteredData.reduce((sum, item) => sum + item.soLopHocPhan, 0);
  const tongSinhVien = filteredData.reduce((sum, item) => sum + item.tongSinhVien, 0);
  const sinhVienTrungBinhTong = tongSoLop > 0 ? tongSinhVien / tongSoLop : 0;

  return (
    <Row gutter={16} style={{ marginBottom: '24px' }}>
      <Col span={6}>
        <Card>
          <Statistic title="Tổng số lớp mở" prefix={<BookOutlined />} valueStyle={{ color: '#3f8600' }}
            value={tongSoLop} />
        </Card>
      </Col>
      <Col span={6}>
        <Card>
          <Statistic title="Tổng số sinh viên" prefix={<TeamOutlined />} valueStyle={{ color: '#1890ff' }}
            value={tongSinhVien} />
        </Card>
      </Col>
      <Col span={6}>
        <Card>
          <Statistic title="SV trung bình/lớp" prefix={<AccountBookOutlined />} valueStyle={{ color: '#722ed1' }}
            value={(sinhVienTrungBinhTong ?? 0)?.toFixed(2)} />
        </Card>
      </Col>
      <Col span={6}>
        {/* {selectedKhoa}
        {JSON.stringify(filteredData, null, 2)} */}
        <Card>
          <Statistic title="Số học phần" prefix={<BookOutlined />} valueStyle={{ color: '#eb2f96' }}
            value={selectedKhoa == 'all' ? thongKeHocPhan.length : filteredData[0]?.soLopHocPhan} />
        </Card>
      </Col>
    </Row>
  )
}

export default OverallStats;