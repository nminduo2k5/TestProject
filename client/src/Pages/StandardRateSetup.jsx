import React from 'react';
import { Layout, Menu, Card, Typography, Breadcrumb } from 'antd';
import { 
  DollarOutlined, 
  UserOutlined, 
  TeamOutlined, 
  CalculatorOutlined,
  SettingOutlined,
  HomeOutlined
} from '@ant-design/icons';

const { Header, Sider, Content } = Layout;
const { Title } = Typography;

// UC3.1 - Thiết lập định mức tiền theo tiết
const StandardRateSetup = () => {
  return (
    <Card title="Thiết lập Định mức Tiền theo Tiết" className="mb-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold mb-3 text-blue-700">Định mức cơ bản</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center p-3 bg-white rounded border">
              <span className="font-medium">Tiết lý thuyết:</span>
              <span className="text-blue-600 font-bold">150,000 VNĐ</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-white rounded border">
              <span className="font-medium">Tiết thực hành:</span>
              <span className="text-blue-600 font-bold">120,000 VNĐ</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-white rounded border">
              <span className="font-medium">Tiết thí nghiệm:</span>
              <span className="text-blue-600 font-bold">130,000 VNĐ</span>
            </div>
          </div>
        </div>
        
        <div className="bg-green-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold mb-3 text-green-700">Cập nhật định mức</h3>
          <div className="space-y-3">
            <div>
              <label className="block text-sm font-medium mb-1">Loại tiết:</label>
              <select className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option>Lý thuyết</option>
                <option>Thực hành</option>
                <option>Thí nghiệm</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Số tiền (VNĐ):</label>
              <input 
                type="number" 
                className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Nhập số tiền"
              />
            </div>
            <button className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700 transition-colors">
              Cập nhật định mức
            </button>
          </div>
        </div>
      </div>
    </Card>
  );
};

// UC3.2 - Thiết lập hệ số giáo viên
const TeacherCoefficientSetup = () => {
  const teacherData = [
    { id: 1, name: 'TS. Nguyễn Văn A', degree: 'Tiến sĩ', experience: '15 năm', coefficient: 2.5 },
    { id: 2, name: 'ThS. Trần Thị B', degree: 'Thạc sĩ', experience: '8 năm', coefficient: 2.0 },
    { id: 3, name: 'CN. Lê Văn C', degree: 'Cử nhân', experience: '3 năm', coefficient: 1.5 },
  ];

  return (
    <Card title="Thiết lập Hệ số Giáo viên" className="mb-4">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <h3 className="text-lg font-semibold mb-3">Danh sách Giáo viên</h3>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse border border-gray-300">
              <thead>
                <tr className="bg-gray-100">
                  <th className="border border-gray-300 p-3 text-left">Tên giáo viên</th>
                  <th className="border border-gray-300 p-3 text-left">Bằng cấp</th>
                  <th className="border border-gray-300 p-3 text-left">Kinh nghiệm</th>
                  <th className="border border-gray-300 p-3 text-center">Hệ số</th>
                  <th className="border border-gray-300 p-3 text-center">Thao tác</th>
                </tr>
              </thead>
              <tbody>
                {teacherData.map((teacher) => (
                  <tr key={teacher.id} className="hover:bg-gray-50">
                    <td className="border border-gray-300 p-3">{teacher.name}</td>
                    <td className="border border-gray-300 p-3">{teacher.degree}</td>
                    <td className="border border-gray-300 p-3">{teacher.experience}</td>
                    <td className="border border-gray-300 p-3 text-center">
                      <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded font-bold">
                        {teacher.coefficient}
                      </span>
                    </td>
                    <td className="border border-gray-300 p-3 text-center">
                      <button className="bg-orange-500 text-white px-3 py-1 rounded text-sm hover:bg-orange-600">
                        Sửa
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        
        <div className="bg-yellow-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold mb-3 text-yellow-700">Quy định hệ số</h3>
          <div className="space-y-3">
            <div className="bg-white p-3 rounded border">
              <div className="font-medium text-sm text-gray-600">Tiến sĩ</div>
              <div className="text-lg font-bold text-yellow-600">2.0 - 3.0</div>
            </div>
            <div className="bg-white p-3 rounded border">
              <div className="font-medium text-sm text-gray-600">Thạc sĩ</div>
              <div className="text-lg font-bold text-yellow-600">1.5 - 2.5</div>
            </div>
            <div className="bg-white p-3 rounded border">
              <div className="font-medium text-sm text-gray-600">Cử nhân</div>
              <div className="text-lg font-bold text-yellow-600">1.0 - 2.0</div>
            </div>
          </div>
          
          <div className="mt-4 pt-4 border-t">
            <h4 className="font-medium mb-2">Cập nhật hệ số</h4>
            <div className="space-y-2">
              <select className="w-full p-2 border rounded text-sm">
                <option>Chọn giáo viên</option>
                <option>TS. Nguyễn Văn A</option>
                <option>ThS. Trần Thị B</option>
              </select>
              <input 
                type="number" 
                step="0.1"
                className="w-full p-2 border rounded text-sm"
                placeholder="Nhập hệ số"
              />
              <button className="w-full bg-yellow-600 text-white py-2 rounded text-sm hover:bg-yellow-700">
                Cập nhật
              </button>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};

// UC3.3 - Thiết lập hệ số lớp
const ClassCoefficientSetup = () => {
  const classData = [
    { id: 1, code: 'IT001', name: 'Lập trình căn bản', students: 45, coefficient: 1.2 },
    { id: 2, code: 'IT002', name: 'Cấu trúc dữ liệu', students: 38, coefficient: 1.1 },
    { id: 3, code: 'IT003', name: 'Cơ sở dữ liệu', students: 52, coefficient: 1.3 },
  ];

  return (
    <Card title="Thiết lập Hệ số Lớp" className="mb-4">
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-3">
          <h3 className="text-lg font-semibold mb-3">Danh sách Lớp học phần</h3>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse border border-gray-300">
              <thead>
                <tr className="bg-gray-100">
                  <th className="border border-gray-300 p-3 text-left">Mã lớp</th>
                  <th className="border border-gray-300 p-3 text-left">Tên học phần</th>
                  <th className="border border-gray-300 p-3 text-center">Sĩ số</th>
                  <th className="border border-gray-300 p-3 text-center">Hệ số</th>
                  <th className="border border-gray-300 p-3 text-center">Thao tác</th>
                </tr>
              </thead>
              <tbody>
                {classData.map((cls) => (
                  <tr key={cls.id} className="hover:bg-gray-50">
                    <td className="border border-gray-300 p-3 font-mono text-sm">{cls.code}</td>
                    <td className="border border-gray-300 p-3">{cls.name}</td>
                    <td className="border border-gray-300 p-3 text-center">{cls.students}</td>
                    <td className="border border-gray-300 p-3 text-center">
                      <span className="bg-purple-100 text-purple-800 px-2 py-1 rounded font-bold">
                        {cls.coefficient}
                      </span>
                    </td>
                    <td className="border border-gray-300 p-3 text-center">
                      <button className="bg-purple-500 text-white px-3 py-1 rounded text-sm hover:bg-purple-600">
                        Sửa
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        
        <div className="bg-purple-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold mb-3 text-purple-700">Quy định hệ số theo sĩ số</h3>
          <div className="space-y-3">
            <div className="bg-white p-3 rounded border">
              <div className="font-medium text-sm text-gray-600">30 sinh viên</div>
              <div className="text-lg font-bold text-purple-600">1.0</div>
            </div>
            <div className="bg-white p-3 rounded border">
              <div className="font-medium text-sm text-gray-600">30-50 sinh viên</div>
              <div className="text-lg font-bold text-purple-600">1.1-1.2</div>
            </div>
            <div className="bg-white p-3 rounded border">
              <div className="font-medium text-sm text-gray-600"> 50 sinh viên</div>
              <div className="text-lg font-bold text-purple-600">1.3-1.5</div>
            </div>
          </div>
          
          <div className="mt-4 pt-4 border-t">
            <h4 className="font-medium mb-2">Tự động tính hệ số</h4>
            <button className="w-full bg-purple-600 text-white py-2 rounded text-sm hover:bg-purple-700 mb-2">
              Tính hệ số tự động
            </button>
            
            <h4 className="font-medium mb-2">Cập nhật thủ công</h4>
            <div className="space-y-2">
              <select className="w-full p-2 border rounded text-sm">
                <option>Chọn lớp</option>
                <option>IT001 - Lập trình căn bản</option>
                <option>IT002 - Cấu trúc dữ liệu</option>
              </select>
              <input 
                type="number" 
                step="0.1"
                className="w-full p-2 border rounded text-sm"
                placeholder="Nhập hệ số"
              />
              <button className="w-full bg-purple-600 text-white py-2 rounded text-sm hover:bg-purple-700">
                Cập nhật
              </button>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};

// UC3.4 - Tính tiền dạy cho giáo viên
const TeacherSalaryCalculation = () => {
  const salaryData = [
    { 
      teacher: 'TS. Nguyễn Văn A', 
      classes: ['IT001', 'IT003'], 
      totalHours: 60, 
      coefficient: 2.5, 
      totalSalary: 22500000 
    },
    { 
      teacher: 'ThS. Trần Thị B', 
      classes: ['IT002'], 
      totalHours: 30, 
      coefficient: 2.0, 
      totalSalary: 9900000 
    },
  ];

  return (
    <Card title="Tính Tiền Dạy cho Giáo viên" className="mb-4">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold">Bảng lương giảng dạy</h3>
            <div className="flex gap-2">
              <select className="p-2 border rounded">
                <option>Kì học 1 - 2024</option>
                <option>Kì học 2 - 2024</option>
              </select>
              <button className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                Tính lương
              </button>
            </div>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full border-collapse border border-gray-300">
              <thead>
                <tr className="bg-gray-100">
                  <th className="border border-gray-300 p-3 text-left">Giáo viên</th>
                  <th className="border border-gray-300 p-3 text-left">Lớp dạy</th>
                  <th className="border border-gray-300 p-3 text-center">Tổng tiết</th>
                  <th className="border border-gray-300 p-3 text-center">Hệ số</th>
                  <th className="border border-gray-300 p-3 text-right">Tổng lương</th>
                </tr>
              </thead>
              <tbody>
                {salaryData.map((item, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="border border-gray-300 p-3 font-medium">{item.teacher}</td>
                    <td className="border border-gray-300 p-3">
                      <div className="flex flex-wrap gap-1">
                        {item.classes.map((cls, i) => (
                          <span key={i} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                            {cls}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="border border-gray-300 p-3 text-center">{item.totalHours}</td>
                    <td className="border border-gray-300 p-3 text-center">{item.coefficient}</td>
                    <td className="border border-gray-300 p-3 text-right font-bold text-green-600">
                      {item.totalSalary.toLocaleString('vi-VN')} VNĐ
                    </td>
                  </tr>
                ))}
              </tbody>
              <tfoot>
                <tr className="bg-green-50">
                  <td colSpan="4" className="border border-gray-300 p-3 text-right font-bold">
                    Tổng chi phí giảng dạy:
                  </td>
                  <td className="border border-gray-300 p-3 text-right font-bold text-green-700">
                    32,400,000 VNĐ
                  </td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>
        
        <div className="bg-green-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold mb-3 text-green-700">Công thức tính</h3>
          <div className="bg-white p-4 rounded border mb-4">
            <div className="text-center">
              <div className="text-sm text-gray-600 mb-2">Lương = </div>
              <div className="font-bold text-green-600">
                Định mức × Số tiết × Hệ số GV × Hệ số lớp
              </div>
            </div>
          </div>
          
          <h4 className="font-medium mb-3">Chi tiết tính toán</h4>
          <div className="space-y-3">
            <div className="bg-white p-3 rounded border">
              <div className="text-sm text-gray-600">Định mức cơ bản</div>
              <div className="font-bold">150,000 VNĐ/tiết</div>
            </div>
            <div className="bg-white p-3 rounded border">
              <div className="text-sm text-gray-600">Hệ số giáo viên</div>
              <div className="font-bold">1.0 - 3.0</div>
            </div>
            <div className="bg-white p-3 rounded border">
              <div className="text-sm text-gray-600">Hệ số lớp</div>
              <div className="font-bold">1.0 - 1.5</div>
            </div>
          </div>
          
          <div className="mt-4 pt-4 border-t">
            <h4 className="font-medium mb-2">Xuất báo cáo</h4>
            <div className="space-y-2">
              <button className="w-full bg-blue-600 text-white py-2 rounded text-sm hover:bg-blue-700">
                Xuất Excel
              </button>
              <button className="w-full bg-red-600 text-white py-2 rounded text-sm hover:bg-red-700">
                Xuất PDF
              </button>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};

// Component chính
const TeachingSalarySystem = () => {
  const [selectedMenu, setSelectedMenu] = React.useState('overview');

  const menuItems = [
    {
      key: 'overview',
      icon: <HomeOutlined />,
      label: 'Tổng quan',
    },
    {
      key: 'standard-rate',
      icon: <DollarOutlined />,
      label: 'Định mức tiền tiết',
    },
    {
      key: 'teacher-coefficient', 
      icon: <UserOutlined />,
      label: 'Hệ số giáo viên',
    },
    {
      key: 'class-coefficient',
      icon: <TeamOutlined />,
      label: 'Hệ số lớp',
    },
    {
      key: 'salary-calculation',
      icon: <CalculatorOutlined />,
      label: 'Tính tiền dạy',
    },
  ];

  const renderContent = () => {
    switch (selectedMenu) {
      case 'standard-rate':
        return <StandardRateSetup />;
      case 'teacher-coefficient':
        return <TeacherCoefficientSetup />;
      case 'class-coefficient':
        return <ClassCoefficientSetup />;
      case 'salary-calculation':
        return <TeacherSalaryCalculation />;
      default:
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card className="text-center bg-gradient-to-br from-blue-500 to-blue-600 text-white">
              <DollarOutlined className="text-4xl mb-2" />
              <div className="text-2xl font-bold">150,000</div>
              <div className="text-sm opacity-90">VNĐ/tiết chuẩn</div>
            </Card>
            <Card className="text-center bg-gradient-to-br from-green-500 to-green-600 text-white">
              <UserOutlined className="text-4xl mb-2" />
              <div className="text-2xl font-bold">45</div>
              <div className="text-sm opacity-90">Giáo viên</div>
            </Card>
            <Card className="text-center bg-gradient-to-br from-purple-500 to-purple-600 text-white">
              <TeamOutlined className="text-4xl mb-2" />
              <div className="text-2xl font-bold">128</div>
              <div className="text-sm opacity-90">Lớp học phần</div>
            </Card>
            <Card className="text-center bg-gradient-to-br from-orange-500 to-orange-600 text-white">
              <CalculatorOutlined className="text-4xl mb-2" />
              <div className="text-2xl font-bold">2.4B</div>
              <div className="text-sm opacity-90">VNĐ tổng chi phí</div>
            </Card>
          </div>
        );
    }
  };

  const getBreadcrumb = () => {
    const breadcrumbMap = {
      'overview': 'Tổng quan',
      'standard-rate': 'Định mức tiền tiết',
      'teacher-coefficient': 'Hệ số giáo viên', 
      'class-coefficient': 'Hệ số lớp',
      'salary-calculation': 'Tính tiền dạy',
    };
    return breadcrumbMap[selectedMenu] || 'Tổng quan';
  };

  return (
    <Layout className="min-h-screen">
      <Header className="bg-white shadow-md px-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <SettingOutlined className="text-2xl text-blue-600 mr-3" />
            <Title level={3} className="!mb-0 !text-gray-800">
              Hệ thống Tính Tiền Dạy
            </Title>
          </div>
          <div className="text-sm text-gray-600">
            Kì học: <span className="font-semibold">1/2024-2025</span>
          </div>
        </div>
      </Header>
      
      <Layout>
        <Sider width={250} className="bg-white shadow-lg">
          <Menu
            mode="inline"
            selectedKeys={[selectedMenu]}
            className="h-full border-none"
            items={menuItems}
            onClick={({ key }) => setSelectedMenu(key)}
          />
        </Sider>
        
        <Layout className="bg-gray-50">
          <div className="p-6">
            <Breadcrumb className="mb-4">
              <Breadcrumb.Item>
                <HomeOutlined />
              </Breadcrumb.Item>
              <Breadcrumb.Item>Quản lý tài chính</Breadcrumb.Item>
              <Breadcrumb.Item>{getBreadcrumb()}</Breadcrumb.Item>
            </Breadcrumb>
            
            <Content>
              {renderContent()}
            </Content>
          </div>
        </Layout>
      </Layout>
    </Layout>
  );
};

export default TeachingSalarySystem;