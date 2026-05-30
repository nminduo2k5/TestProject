import { BarChartOutlined } from '@ant-design/icons';
import { Card, Table } from 'antd';
import { useData } from "./context";


function DataTable() {
  const [{
    selectedKhoa, thongKeHocPhan
  }, dispatch] = useData();

  // console.log(thongKeHocPhan)

  const columns = [
    { title: 'Mã học phần', dataIndex: 'maHocPhan', key: 'maHocPhan', width: 120, },
    { title: 'Tên học phần', dataIndex: 'tenHocPhan', key: 'tenHocPhan', width: 200, },
    { title: 'Số lớp mở', dataIndex: 'soLopHocPhan', key: 'soLopHocPhan', width: 100, align: 'center', },
    { title: 'Tổng sinh viên', dataIndex: 'tongSinhVien', key: 'tongSinhVien', width: 120, align: 'center', },
    {
      title: 'SV trung bình/lớp', dataIndex: 'trungBinhSinhVienLop', key: 'trungBinhSinhVienLop', width: 150, align: 'center',
      render: data => (data ?? 0).toFixed(0)
    },
    { title: 'Khoa', dataIndex: 'tenKhoa', key: 'tenKhoa', width: 100, align: 'center', }
  ];

  const filteredData = thongKeHocPhan.filter(item => {
    return (selectedKhoa == 'all' || item.khoaId === selectedKhoa);
  });

  return (
    <Card
      title={
        <span style={{ fontSize: '16px', fontWeight: 'bold', color: '#2A7ED7' }}>
          <BarChartOutlined style={{ marginRight: '8px' }} />
          Chi tiết thống kê theo học phần
        </span>
      }>
      <Table
        columns={columns}
        dataSource={filteredData}
        scroll={{ x: 800 }}
        size="middle"
        pagination={{
          showSizeChanger: true,
          showQuickJumper: true,
          showTotal: (total, range) => `${range[0]}-${range[1]} của ${total} học phần`,
        }}
      />
    </Card>
  )
}

export default DataTable;