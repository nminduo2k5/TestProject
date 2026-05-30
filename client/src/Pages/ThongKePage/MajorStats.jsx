import { ManOutlined, TeamOutlined, WomanOutlined } from '@ant-design/icons';
import { Card, Select, Space, Statistic, Table, Tabs, Typography } from 'antd';
import { useContext, useEffect, useState } from 'react';
import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts';
import { Context } from './context';

const { Title } = Typography;

const COLORS = [
  '#FF6384', // Hồng đỏ
  '#36A2EB', // Xanh dương sáng
  '#FFCE56', // Vàng sáng
  '#4BC0C0', // Xanh ngọc
  '#9966FF', // Tím
  '#FF9F40', // Cam
  '#C9CBCF', // Xám sáng
  '#00A950', // Xanh lá đậm
  '#E74C3C', // Đỏ tươi
  '#2ECC71'  // Xanh lá tươi
];
function MajorStats() {
  const [state,] = useContext(Context);
  const [selectedFaculty, setSelectedFaculty] = useState(null);

  useEffect(() => {
    if (state.khoa && state.khoa.length > 0)
      setSelectedFaculty(state.khoa[0].maKhoa);

  }, [state]);

  const genderData = state.gioiTinh.filter(i => i.maKhoa === selectedFaculty).map(i => ({ name: i.gioiTinhText, value: i.soGiangVien }))
  const degreeData = state.bangCap.filter(i => i.maKhoa === selectedFaculty).map(i => ({ name: i.tenBangCap, value: i.soGiangVien }))
  const overallData = {
    totalLecturers: state.gioiTinh.filter(i => i.maKhoa === selectedFaculty).reduce((acc, item) => acc + item.soGiangVien, 0),
    maleCount: state.gioiTinh.filter(i => i.maKhoa === selectedFaculty && i.gioiTinhText === 'Nam').reduce((acc, item) => acc + item.soGiangVien, 0),
    femaleCount: state.gioiTinh.filter(i => i.maKhoa === selectedFaculty && i.gioiTinhText === 'Nữ').reduce((acc, item) => acc + item.soGiangVien, 0),
  }

  const facultyDetails = state.gioiTinh.filter(i => i.maKhoa === selectedFaculty).map(i => ({ name: i.gioiTinhText, value: i.soGiangVien }))

  const columns = [
    { title: <p className='text-center'>Tên khoa</p>, fixed: 'left', dataIndex: 'name', key: 'name', render: _ => <p className="text-blue-600 font-semibold">{_}</p>, width: 220 },
    { title: <p className='text-center'>Tổng số</p>, dataIndex: 'totalLecturers', key: 'totalLecturers', width: 70, render: _ => <p className="text-center">{_}</p> },
    { title: <p className='text-center'>Nam</p>, dataIndex: 'maleCount', key: 'maleCount', width: 50, render: _ => <p className="text-center">{_}</p> },
    { title: <p className='text-center'>Nữ</p>, dataIndex: 'femaleCount', key: 'femaleCount', width: 50, render: _ => <p className="text-center">{_}</p> },
    ...(state.bC?.map(i => ({ title: <p className='text-center'>{i.tenBangCap}</p>, dataIndex: i.tenVietTat, key: i.maBangCap, width: 100, render: _ => <p className="text-center">{_}</p> })) || [])
  ];


  const tabs = [
    {
      key: '1', label: 'Danh sách khoa',
      children: (
        <Table
          columns={columns}
          rowKey="id"
          pagination={false}
          bordered
          size='small'
          scroll={{ x: 'max-content' }}
          dataSource={state.khoa?.map(i => ({
            id: i.maKhoa,
            key: i.maKhoa,
            name: i.tenKhoa,
            totalLecturers: state.gioiTinh.filter(j => j.maKhoa === i.maKhoa).reduce((acc, item) => acc + item.soGiangVien, 0),
            maleCount: state.gioiTinh.filter(j => j.maKhoa === i.maKhoa && j.gioiTinhText === 'Nam').reduce((acc, item) => acc + item.soGiangVien, 0),
            femaleCount: state.gioiTinh.filter(j => j.maKhoa === i.maKhoa && j.gioiTinhText === 'Nữ').reduce((acc, item) => acc + item.soGiangVien, 0),
            ...Object.fromEntries(state.bC.map(k => [k.tenVietTat, state.bangCap.filter(j => j.maKhoa === i.maKhoa && j.maBangCap === k.maBangCap)[0]?.soGiangVien || 0]))
          }))} />
      ),
    },
    {
      key: '2', label: 'Chi tiết khoa',
      children:
        <Space direction="vertical" className="w-full">
          <div className="mb-4">
            <Select
              className="ml-4 w-64"
              placeholder="Chọn khoa để xem chi tiết"
              onChange={value => setSelectedFaculty(value)}
              value={selectedFaculty}
              options={state.khoa?.map(khoa => ({ value: khoa.maKhoa, label: khoa.tenKhoa }))} />
          </div>

          <Title level={4}>{facultyDetails.name}</Title>
          <div gutter={[16, 16]} className="mb-4 grid grid-cols-3 gap-10">
            <Card className="bg-blue-50">
              <Statistic title="Tổng số giáo viên" value={overallData.totalLecturers} prefix={<TeamOutlined />} valueStyle={{ color: '#1890ff' }} />
            </Card>
            <Card className="bg-green-50">
              <Statistic title="Giáo viên nam" value={overallData.maleCount} prefix={<ManOutlined />} valueStyle={{ color: '#3f8600' }} suffix={`(${Math.round(overallData.maleCount / overallData.totalLecturers * 100)}%)`} />
            </Card>
            <Card className="bg-pink-50">
              <Statistic title="Giáo viên nữ" value={overallData.femaleCount} prefix={<WomanOutlined />} valueStyle={{ color: '#eb2f96' }} suffix={`(${Math.round(overallData.femaleCount / overallData.totalLecturers * 100)}%)`} />
            </Card>
          </div>

          <div className='grid grid-cols-2 gap-5'>

            <Card title="Phân bố giới tính">
              <ResponsiveContainer width="100%" height={400}>
                <PieChart>
                  <Pie
                    cx="50%" cy="50%" labelLine={false} outerRadius={110} fill="#8884d8" dataKey="value"
                    data={genderData}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(2)}%`}>
                    <Cell fill="#1890ff" />
                    <Cell fill="#eb2f96" />
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </Card>


            <Card title="Phân bố bằng cấp">
              <ResponsiveContainer width="100%" height={400}>
                <PieChart>
                  <Pie data={degreeData}
                    cx="50%" cy="50%" labelLine={false} outerRadius={110} fill="#8884d8" dataKey="value"
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(2)}%`}>
                    {degreeData.map((_, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </Card>

          </div>

        </Space>,
    },
  ]
  return <Tabs defaultActiveKey="1" className="mb-8 " items={tabs} />
}

export default MajorStats