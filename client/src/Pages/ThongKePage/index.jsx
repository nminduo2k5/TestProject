import { Typography } from 'antd';
import axios from 'axios';
import { useEffect, useReducer } from 'react';

const { Title } = Typography;

import MajorStats from './MajorStats';
import OverallDegree from './OverallDegree';
import OverallGender from './OverallGender';
import OverallMajor from './OverallMajor';
import OverallStats from './OverallStats';
import { Context, initialState, reducer } from './context';


function ThongKePage() {
  const [state, dispatch] = useReducer(reducer, initialState);

  useEffect(() => {
    // Giả lập việc lấy dữ liệu từ API
    axios.get('http://localhost:5249/thong-ke-giao-vien')
      .then(response => {
        // Giả lập dữ liệu trả về từ API
        const data = response.data;
        console.log(data)

        // Cập nhật dữ liệu vào state
        dispatch({ type: 'updateData', payload: data });
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  return (
    <Context.Provider value={[state, dispatch]}>
      <div className="min-h-screen bg-gray-100 p-6">
        <div className="rounded-lg shadow p-6 bg-white">

          <Title level={3} className="mb-6">Thống kê giáo viên toàn trường</Title>

          <OverallStats />
          {/* <Divider orientation="left">Thống kê theo bằng cấp</Divider> */}
          <div className="mb-8 grid grid-cols-2 gap-5">
            <OverallDegree />
            <OverallGender />
          </div>

          <OverallMajor />

          <MajorStats />
        </div>
      </div>
    </Context.Provider>
  );
};

export default ThongKePage;