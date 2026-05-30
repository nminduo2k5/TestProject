import { faPen, faTrash } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button, message, Popconfirm, Space, Table } from "antd";
import { useEffect } from "react";

import { DeleteHocPhan, GetHocPhan } from "@/api/hocphanApi";
import { useData } from "./context";

function TableHeader({ children }) {
  return (
    <p className="text-lg font-semibold">{children} </p>
  )
}

function DataTable() {
  const [{ hocPhanList, selectedKhoaId }, dispatch] = useData()

  useEffect(function () {
    GetHocPhan().then(data => dispatch({ type: 'updateHocPhanList', payload: data }))
  }, [dispatch])

  const columns = [
    { title: <TableHeader>STT</TableHeader>, key: 'stt', width: 60, align: 'center', render: (_, __, index) => index + 1, },
    { title: <TableHeader>Mã học phần</TableHeader>, dataIndex: 'maHocPhan', key: 'maHocPhan', width: 120, },
    { title: <TableHeader>Tên học phần</TableHeader>, dataIndex: 'tenHocPhan', key: 'tenHocPhan', width: 200, },
    { title: <TableHeader>Số tín chỉ</TableHeader>, dataIndex: 'soTinChi', key: 'soTinChi', width: 100, align: 'center', },
    { title: <TableHeader>Hệ số</TableHeader>, dataIndex: 'heSoHocPhan', key: 'heSoHocPhan', width: 80, align: 'center', },
    { title: <TableHeader>Số tiết</TableHeader>, dataIndex: 'soTiet', key: 'soTiet', width: 80, align: 'center', },
    selectedKhoaId == 'all' ? { title: <TableHeader>Khoa</TableHeader>, dataIndex: 'tenKhoa', key: 'tenKhoa', width: 120, } : null,
    {
      title: <TableHeader>Thao tác</TableHeader>, key: 'action', width: 100, align: 'center', fixed: 'right',
      render: (_, record) => (
        <Space>
          <Button variant="outlined" color="blue" icon={<FontAwesomeIcon icon={faPen} />}
            onClick={() => {
              dispatch([
                { type: "updateModal", payload: true },
                { type: "updateModalMode", payload: "edit" },
                { type: "updateEditForm", payload: record }
              ])
            }} />
          <Popconfirm title="Bạn có chắc chắn muốn xóa?" okText="Có" cancelText="Không"
            onConfirm={async () => {
              await DeleteHocPhan(record.id)
              const data = await GetHocPhan()

              dispatch({ type: "updateHocPhanList", payload: data })
              message.success("Xóa học phần thành công!")
            }}>
            <Button variant="outlined" color="red" icon={<FontAwesomeIcon icon={faTrash} />} />
          </Popconfirm>
        </Space>
      ),
    },
  ].filter(i => !!i);

  return (
    <div className='rounded bg-white shadow'>
      <Table
        dataSource={hocPhanList.filter(i => (selectedKhoaId == 'all' || i.khoaId == selectedKhoaId))}
        columns={columns}
        size="small"
        bordered
        scroll={{ x: 800 }}
        pagination={{
          pageSize: 10,
          showSizeChanger: false,
          showQuickJumper: false,
          showTotal: (total, range) => `Hiển thị ${range[0]}-${range[1]} trong tổng số ${total} bản ghi`,
        }} />
    </div>
  )
}

export default DataTable