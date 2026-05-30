import { ManOutlined, TeamOutlined, WomanOutlined } from '@ant-design/icons';
import { Card, Statistic } from 'antd';
import { Context } from './context';
import { useContext } from 'react';

function OverallStats() {
  const [state,] = useContext(Context);
  const data = state.processData.gender;
  const totalLecturers = state.processData.totalLecturers;
  // console.log(totalLecturers)

  return (
    <div className="mb-8 grid grid-cols-3 gap-3">
      <div>
        <Card className="bg-blue-50">
          <Statistic title="Tổng số giáo viên" value={totalLecturers} prefix={<TeamOutlined />} valueStyle={{ color: '#1890ff' }} />
        </Card>
      </div>
      <div>
        <Card className="bg-green-50">
          <Statistic
            title="Giáo viên nam"
            value={data.maleCount}
            prefix={<ManOutlined />}
            valueStyle={{ color: '#3f8600' }}
            suffix={`(${(data.maleCount / totalLecturers * 100).toFixed(2)}%)`} />
        </Card>
      </div>
      <div>
        <Card className="bg-pink-50">
          <Statistic
            title="Giáo viên nữ"
            value={data.femaleCount}
            prefix={<WomanOutlined />}
            valueStyle={{ color: '#eb2f96' }}
            suffix={`(${(data.femaleCount / totalLecturers * 100).toFixed(2)}%)`} />
        </Card>
      </div>
    </div>

  )
}

export default OverallStats