import { UserOutlined } from '@ant-design/icons';
import { Card, Typography } from 'antd';
import { useContext } from 'react';
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

function OverallGender() {
  const [state,] = useContext(Context);

  const data = state.processData.gender;
  const genderData = [
    { name: 'Nam', value: data.maleCount },
    { name: 'Nữ', value: data.femaleCount },
  ];
  return (
    <Card>
      <div className="flex items-center mb-4">
        <div className="w-8 h-8 bg-pink-500 flex items-center justify-center rounded-full mr-2">
          <UserOutlined className="text-white" />
        </div>
        <Title level={4} className="m-0">Phân bố theo giới tính</Title>
      </div>
      <ResponsiveContainer width="100%" height={400}>
        <PieChart>
          <Pie data={genderData} cx="50%" cy="50%" labelLine={false} outerRadius={150} fill="#8884d8" dataKey="value"
            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(2)}%`}>
            {genderData.map((entry, index) => (<Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>

    </Card>
  )
}

export default OverallGender