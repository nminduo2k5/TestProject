import { ChevronDown, Phone, MessageSquare, Mail } from "lucide-react";
import logo from '../assets/Logo.png'
import pic2 from '../assets/pic2.png'

export default function MTMLoginPage() {
  return (
    <div className="min-h-screen flex flex-col" style={{ backgroundColor: "#F8F5FD" }}>
      <div className="flex-grow flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl w-full flex flex-col md:flex-row gap-8 lg:gap-16">
          {/* Left Column - Logo and Illustration */}
          <div className="flex flex-col items-center md:items-start">
            <div className="w-64 mx-auto">
              <img src={logo} alt="MTM University Logo" className="w-full" />
            </div>

            <div className="w-full max-w-md">
              <img src={pic2} />
            </div>
          </div>

          {/* Right Column - Login Form */}
          <div className="flex-1">
            <div className="text-center mb-8">
              <h1 className="text-2xl font-bold text-red-700">TRƯỜNG ĐẠI HỌC MTM</h1>
              <h2 className="text-xl font-bold text-navy-800">PHẦN MỀM TÍNH TIỀN DẠY CỦA</h2>
              <h2 className="text-xl font-bold text-navy-800">GIẢNG VIÊN</h2>
            </div>

            <div className="mb-6">
              <label className="block text-gray-700 mb-1">Chọn vai trò của bạn</label>
              <div className="relative">
                <select className="w-full border border-gray-300 rounded-md py-3 px-4 appearance-none focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option>Giảng viên</option>
                  <option>Quản trị viên</option>
                </select>
                <div className="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
                  <ChevronDown className="h-5 w-5 text-gray-400" />
                </div>
              </div>
            </div>

            <div className="mb-6">
              <label className="block text-gray-700 mb-1">Tên đăng nhập*</label>
              <input
                type="text"
                className="w-full border border-gray-300 rounded-md py-3 px-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="mb-8">
              <label className="block text-gray-700 mb-1">Mật khẩu*</label>
              <input
                type="password"
                className="w-full border border-gray-300 rounded-md py-3 px-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <button className="w-full bg-navy-800 text-white rounded-md py-3 font-medium hover:bg-navy-900 transition duration-200">
              Đăng nhập
            </button>

            <div className="mt-12 text-center text-gray-600 text-sm">
              <p>Copyright ©2025, MTM University. All rights.</p>
              <p className="mt-2">
                Phòng Tài chính Kế toán - Địa chỉ: Tầng 12, tòa ABC,<br />
                Trường đại học MTM, Hà Nội, Việt Nam
              </p>
            </div>

            <div className="mt-8 flex justify-center space-x-8">
              <a href="#" className="text-navy-800 hover:text-navy-600">
                <Phone className="h-6 w-6" />
              </a>
              <a href="#" className="text-navy-800 hover:text-navy-600">
                <MessageSquare className="h-6 w-6" />
              </a>
              <a href="#" className="text-navy-800 hover:text-navy-600">
                <Mail className="h-6 w-6" />
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}