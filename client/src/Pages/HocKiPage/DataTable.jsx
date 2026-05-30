import { DeleteOutlined, EditOutlined } from '@ant-design/icons';
import { Button, message, Popconfirm, Space, Table, Tag } from 'antd';
import dayjs from 'dayjs';
import { useEffect } from 'react';

import { DeleteHocKy, GetHocKyList } from '@/api/hocKiApi';
import { useData } from './context';
import { faPen, faTrash } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';


function TableHeader({ children }) {
  return <p className='text-lg font-semibold'>{children}</p>
}

function getYear(str) {
  return new Date(str).getFullYear()
}

function DataTable() {
  const [{
    data, kyData, selectedYear
  }, dispatch] = useData()

  useEffect(function () {
    GetHocKyList().then(res => dispatch([
      { type: "updateKyData", payload: res.map((i, j) => ({ ...i, key: j })) }
    ]))
  }, [dispatch])

  const columns = [
    { title: <TableHeader>STT</TableHeader>, dataIndex: 'stt', key: 'stt', width: 50, render: (text, _, i) => <span className='text-lg'>{i + 1}</span> },
    { title: <TableHeader>Tên học kỳ</TableHeader>, dataIndex: 'tenKi', key: 'tenKi', width: 150, render: (text) => <span className='text-lg'>{text}</span> },
    { title: <TableHeader>Năm học</TableHeader>, dataIndex: 'namHoc', key: 'namHoc', width: 120, align: 'center', render: (_, i) => <span className='text-lg'>{getYear(i.thoiGianBatDau)}-{getYear(i.thoiGianBatDau) + 1}</span> },
    { title: <TableHeader>Ngày bắt đầu</TableHeader>, dataIndex: 'thoiGianBatDau', key: 'thoiGianBatDau', width: 120, align: 'center', render: (date) => <span className='text-lg'>{dayjs(date).format('DD/MM/YYYY')}</span> },
    { title: <TableHeader>Ngày kết thúc</TableHeader>, dataIndex: 'thoiGianKetThuc', key: 'thoiGianKetThuc', width: 120, align: 'center', render: (date) => <span className='text-lg'>{dayjs(date).format('DD/MM/YYYY')}</span> },
    {
      title: <TableHeader>Trạng thái</TableHeader>, dataIndex: 'trangThai', key: 'trangThai', width: 120, align: 'center',
      render: (_, entry) => {
        // console.log(entry)
        let color = 'default';
        const tgBatDau = new Date(entry.thoiGianBatDau);
        const tgKetThuc = new Date(entry.thoiGianKetThuc);
        const tgHienTai = new Date();
        let status;
        if (tgBatDau <= tgHienTai && tgHienTai <= tgKetThuc) {
          color = 'green';
          status = 'Đang diễn ra'
        }
        else if (tgBatDau > tgHienTai) {
          color = 'blue';
          status = 'Chưa bắt đầu'
        }
        else if (tgKetThuc < tgHienTai) {
          color = 'red';
          status = 'Đã kết thúc'
        }
        // console.log(status, entry, { tgBatDau, tgKetThuc, tgHienTai }, tgKetThuc < tgHienTai)
        return <Tag color={color}>{status}</Tag>;
      }
    },
    {
      title: <TableHeader>Thao tác</TableHeader>, key: 'action', width: 120, align: 'center',
      render: (_, record) => (
        <Space size="small">
          <Button
            variant="outlined" color="blue" icon={<FontAwesomeIcon icon={faPen} />}
            disabled={new Date(record.thoiGianBatDau) <= new Date()}
            onClick={() => {
              dispatch([
                { type: "updateModelMode", payload: "edit" },
                { type: "updateModel", payload: true },
                { type: "setFormData", payload: { ...record } },
              ])
            }} />
          <Popconfirm title="Bạn có chắc chắn muốn xóa?" okText="Có" cancelText="Không"
            onConfirm={async () => {
              await DeleteHocKy(record.id)
              dispatch([
                { type: "updateKyData", payload: await GetHocKyList() },
                // { type: "updateSelectedYear", payload: 'all' }
              ])
              message.success("Xóa học kỳ thành công!")
            }}>
            <Button disabled={new Date(record.thoiGianBatDau) <= new Date()} variant="outlined" color="red" icon={<FontAwesomeIcon icon={faTrash} />} />
          </Popconfirm>
        </Space>
      ),
    },
  ];
  return (
    <Table className='mt-4'
      columns={columns}
      dataSource={kyData.filter(i => (selectedYear == 'all' || new Date(i.thoiGianBatDau).getFullYear() == selectedYear))}
      pagination={{
        pageSize: 10,
        showSizeChanger: true,
        showQuickJumper: true,
        showTotal: (total, range) => `${range[0]}-${range[1]} của ${total} học kỳ`,
      }} scroll={{ x: 800 }} size="small" />
  )
}

export default DataTable