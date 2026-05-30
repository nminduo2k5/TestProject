import { Table, Tag } from "antd";
import { useData } from "./context";
import { useEffect, useMemo, useState } from "react";
import { GetHocPhanTinhTrang } from "@/api/hocphanApi";

function TableHeader({ children }) {
  return (
    <p className="text-lg font-semibold">{children} </p>
  )
}

function HocPhanDataTable() {
  const [data, setData] = useState([])
  const [{ filterForm }, dispatch] = useData()
  const { khoaId, hocKiId, namHoc, trangThai } = filterForm

  const filterData = useMemo(() => {
    const result = Object.values(data
      .reduce((acc, item) => {
        if (!acc[item.id]) acc[item.id] = { ...item }
        else acc[item.id].soLopHocPhan += (item.soLopHocPhan || 0)
        return acc
      }, {}))

    return result.filter(i =>
      (khoaId == 'all' || i.khoaId == khoaId) &&
      (hocKiId == 'all' || i.hocKiId == "00000000-0000-0000-0000-000000000000" || i.hocKiId == hocKiId) &&
      (namHoc == 'all' || i.thoiGianBatDau == "0001-01-01T00:00:00" || new Date(i.thoiGianBatDau).getFullYear() == namHoc) &&
      (trangThai === 'all' || (i.soLopHocPhan > 0 && trangThai === 'yes') || (i.soLopHocPhan == 0 && trangThai === 'no')))
  }, [data, khoaId, hocKiId, namHoc, trangThai])

  useEffect(function () {
    GetHocPhanTinhTrang().then(res => setData(res))
  }, [])

  const columns = [
    { title: <TableHeader>STT</TableHeader>, key: 'stt', width: 60, align: 'center', render: (_, __, index) => index + 1, },
    { title: <TableHeader>Mã học phần</TableHeader>, dataIndex: 'maHocPhan', key: 'maHocPhan', width: 120, },
    { title: <TableHeader>Tên học phần</TableHeader>, dataIndex: 'tenHocPhan', key: 'tenHocPhan', width: 200, },
    { title: <TableHeader>Khoa</TableHeader>, dataIndex: 'tenKhoa', key: 'tenKhoa', width: 120, },
    { title: <TableHeader>Số tín chỉ</TableHeader>, dataIndex: 'soTinChi', key: 'soTinChi', width: 100, align: 'center', },
    { title: <TableHeader>Hệ số</TableHeader>, dataIndex: 'heSoHocPhan', key: 'heSoHocPhan', width: 80, align: 'center', render: _ => _?.toFixed(2) },
    { title: <TableHeader>Số tiết</TableHeader>, dataIndex: 'soTiet', key: 'soTiet', width: 80, align: 'center', },
    {
      title: <TableHeader>Trạng thái</TableHeader>, dataIndex: 'soTiet', key: 'soTiet', width: 80, align: 'center',
      render: (_, entry) => entry.soLopHocPhan > 0 ? <Tag color="blue">Đã mở lớp</Tag> : <Tag color="purple">Chưa mở lớp</Tag>
    },
  ];

  return (
    <Table
      columns={columns}
      dataSource={filterData}
      size="small"
      bordered
      pagination={{
        pageSize: 10,
        showSizeChanger: false,
        showQuickJumper: false,
        showTotal: (total, range) => `Hiển thị ${range[0]}-${range[1]} trong tổng số ${total} bản ghi`,
      }} />
  )
}

export default HocPhanDataTable