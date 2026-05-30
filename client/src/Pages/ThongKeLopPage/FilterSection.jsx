import { BarChartOutlined } from '@ant-design/icons';
import { Button, Card, Col, Row, Select, Space } from 'antd';
import { useState } from 'react';

import { useData } from './context';
import { GetThongKeLopHocPhanTheoHocKi, GetThongKeLopHocPhanTheoHocPhan } from '@/api/lhpThongKeApi';


function FilterSection() {
  const [{
    selectedKhoa, selectedKy, selectedNam,
    khoaData, namHocData, hocKiData
  }, dispatch] = useData()
  const [namHoc, setNamHoc] = useState('all')

  return (
    <Card style={{ marginBottom: '12px', marginTop: "12px" }}>
      <Row gutter={16}>
        <Col span={6}>
          <div style={{ marginBottom: '8px', fontWeight: 'bold' }}>Khoa:</div>
          <Select
            placeholder="Chọn khoa" style={{ width: '100%' }} allowClear
            value={selectedKhoa || undefined}
            onChange={a => dispatch([{ type: 'updateSelectedKhoa', payload: a }])}
            options={[
              { value: 'all', label: 'Tất cả khoa' },
              ...khoaData.map(k => ({ value: k.id, label: k.tenKhoa }))
            ]} />
        </Col>
        <Col span={6}>
          <div style={{ marginBottom: '8px', fontWeight: 'bold' }}>Năm học:</div>
          <Select
            placeholder="Chọn năm học"
            style={{ width: '100%' }}
            value={selectedNam || undefined}
            onChange={async a => dispatch([
              { type: 'updateData', payload: { key: 'thongKeHocPhan', data: await GetThongKeLopHocPhanTheoHocPhan(new Date(a, 0, 1)) } },
              { type: 'updateSelectedNam', payload: a },
              { type: 'updateSelectedKy', payload: 'all' }
            ])}
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
            disabled={selectedNam == 'all'}
            value={selectedKy || undefined}
            onChange={async (a) => {
              dispatch([
                { type: 'updateData', payload: { key: 'thongKeHocPhan', data: await GetThongKeLopHocPhanTheoHocKi(a) } },
                { type: 'updateSelectedKy', payload: a }
              ])
            }}
            options={[
              { value: 'all', label: 'Tất cả kỳ học' },
              ...hocKiData
                .filter(ky => new Date(ky.thoiGianBatDau).getFullYear() == selectedNam)
                .map(ky => ({ value: ky.id, label: ky.tenKi }))
            ]} />
        </Col>
        <Col span={6}>
          <div style={{ marginBottom: '8px' }}>&nbsp;</div>
          <Space>
            <Button type="primary" icon={<BarChartOutlined />} >
              Thống kê
            </Button>
            <Button type='primary' style={{ backgroundColor: '#19A10A' }}>Xuất báo cáo</Button>
          </Space>
        </Col>
      </Row>
    </Card>
  )
}

export default FilterSection;