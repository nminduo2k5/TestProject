import { faArrowRotateRight, faPen, faPlus, faSearch, faTrash, faUpload } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button, Input, message, Modal, Popconfirm, Select, Table } from "antd";
import axios from "axios";
import { useEffect, useReducer, useState } from "react";

import TableHeader from "@/Components/TableHeader";
import Context, { intitialValue, reducer } from "./context";
import CreateForm from "./CreateForm";
import { getNextIdNumber } from "@/Utils/FormUtils";

function GiaoVienPage() {
  const [messageApi, contextHolder] = message.useMessage();
  const [state, dispatch] = useReducer(reducer, intitialValue)
  const [search, setSearch] = useState("")
  // const [createForm, setCreateForm] = useState(false)

  function updateData() {
    axios.get('http://localhost:5249/GiangVien')
      .then(res => {
        dispatch({ type: "updateGiangVienData", payload: res.data })
        return res.data
      })
      .then(res => {
        dispatch({ type: "updateGVInput", payload: { name: "maGiangVien", value: `GV-${getNextIdNumber(res.map(i => i.maGiangVien))}` } })
        console.log(res.filter(i => i.id == '6fb69d92-313b-41d9-be9b-02fe4146e381'))
      })

    axios.get("http://localhost:5249/Khoa")
      .then(res => dispatch({ type: "updateKhoa", payload: res.data }))
  }

  useEffect(function () {
    updateData()
  }, [])
  const success = m => {
    messageApi.open({ type: 'success', content: m, });
  };
  const error = m => {
    messageApi.open({ type: 'error', content: m, });
  };
  const columns = [
    { title: <TableHeader>STT</TableHeader>, dataIndex: 'stt', width: 5, render: (_, record, index) => <TableHeader>{index + 1}</TableHeader> },
    { title: <TableHeader>Mã số</TableHeader>, dataIndex: 'maGiangVien', key: 'maGiangVien', width: 80, render: i => <div className="text-lg text-center">{i}</div> },
    { title: <TableHeader>Họ tên</TableHeader>, dataIndex: 'tenGiangVien', key: 'tenGiangVien', width: 100, render: i => <div className="text-lg">{i}</div> },
    { title: <TableHeader>Giới tính</TableHeader>, dataIndex: 'gioiTinh', key: 'gioiTinh', width: 80, render: i => <div className="text-lg text-center">{i}</div> },
    { title: <TableHeader>Ngày sinh</TableHeader>, dataIndex: 'sinhNhat', key: 'sinhNhat', width: 100, render: i => <div className="text-lg text-center">{new Date(i).toLocaleDateString()}</div> },
    { title: <TableHeader>Số điện thoại</TableHeader>, dataIndex: 'soDienThoai', key: 'soDienThoai', width: 100, render: i => <div className="text-lg text-center">{i}</div> },
    { title: <TableHeader>Mail</TableHeader>, dataIndex: 'mail', key: 'mail', width: 100, render: i => <div className="text-lg">{i}</div> },
    { title: <TableHeader>Chức vụ</TableHeader>, dataIndex: 'tenChucVu', key: 'tenChucVu', width: 100, render: i => <div className="text-lg text-center">{i}</div> },
    state.viewOption == 'all' && { title: <TableHeader>Khoa</TableHeader>, dataIndex: 'tenKhoa', key: 'tenKhoa', width: 100, render: i => <div className="text-lg text-center">{i}</div> },
    { title: <TableHeader>Bằng cấp</TableHeader>, dataIndex: 'tenBangCap', key: 'tenBangCap', width: 100, render: i => <div className="text-lg text-center">{i}</div> },
    {
      title: <TableHeader>Tùy chọn</TableHeader>, key: 'action', width: 5,
      render: (_, entry) => (
        <div className="flex gap-5 items-center justify-center" >
          <Button data-testid="btn=sua" variant="outlined" color="blue" icon={<FontAwesomeIcon icon={faPen} />}
            onClick={function () {
              // console.log(entry)
              dispatch({
                type: "setEditForm", payload: {
                  giangVien: {
                    maGiangVien: entry.maGiangVien,
                    tenGiangVien: entry.tenGiangVien,
                    gioiTinh: entry.gioiTinh === "Nam" ? 0 : 1,
                    sinhNhat: new Date(entry.sinhNhat),
                    soDienThoai: entry.soDienThoai,
                    mail: entry.mail,
                    bangCapId: entry.idBangCap,
                    id: entry.id
                  },
                  khoaId: entry.idKhoa,
                  chucVuId: entry.idChucVu
                }
              })
              dispatch({ type: "updateInputMode", payload: "update" })
              dispatch({ type: "openForm" })
            }} />
          <Popconfirm
            title="Bạn có chắc chắn muốn xóa giảng viên này không?"
            description="Giảng viên này sẽ bị xóa vĩnh viễn!"
            placement="left"
            onConfirm={() => axios.delete(`http://localhost:5249/GiangVien/${entry.id}`).then(() => {
              success("Xoá giáo viên thành công!")
              updateData()
            })}>
            <Button data-testid="btn-xoa" variant="outlined" color="red" icon={<FontAwesomeIcon icon={faTrash} />} />
          </Popconfirm>
        </div>
      ),
    },
  ].filter(i => !!i);
  console.log(state.giangVienData, state.viewOption, state.khoaData)
  return (
    <Context.Provider value={[state, dispatch]}>
      {contextHolder}
      <div className="p-5 flex flex-col gap-5" >
        <div className="flex justify-between gap-2 items-center">
          <div className="flex gap-5">
            <Select
              // style={{ width: 120 }}
              className="w-60"
              value={state.viewOption}
              onChange={e => dispatch({ type: "updateGiangVienTable", payload: e })}
              options={[
                { value: 'all', label: 'Toàn trường' },
                ...state.khoaData.map(i => ({ value: i.id, label: i.tenKhoa }))
              ]}
            />
          </div>
          <div className="flex justify-end gap-2 items-center">
            <Input placeholder="Tìm kiếm" style={{ width: "200px" }} value={search} onChange={e => setSearch(e.target.value)} />
            <Button variant="link" color="blue" icon={<FontAwesomeIcon icon={faSearch} className="scale-150" />} onClick={async () => {
              const response = await axios.get('http://localhost:5249/GiangVien')
              const result = response.data.filter(i => JSON.stringify(i).includes(search.toLowerCase()))
              if (result.length === 0) error("Không tìm thấy kết quả!")
              dispatch({ type: "updateGiangVienData", payload: result })

            }} />
            <Button data-testid="btn-them" variant="link" color="orange" icon={<FontAwesomeIcon icon={faPlus} className="scale-150" />} onClick={() => {
              dispatch({ type: "openForm" })
              dispatch({ type: "updateInputMode", payload: "create" })
              dispatch({ type: "resetInput" })
            }} />
            <Button variant="link" color="green" icon={<FontAwesomeIcon icon={faUpload} className="scale-150" />} />
            <Button variant="link" color="blue" icon={<FontAwesomeIcon icon={faArrowRotateRight} className="scale-150" />} onClick={updateData} />
          </div>
        </div>

        <Table
          columns={columns}
          dataSource={state.giangVienData.filter(i => state.viewOption === 'all' || i.idKhoa === state.viewOption)}
          pagination={{ pageSize: 10 }}
          size="small"
          bordered
          scroll={{ x: 'max-content' }}
          className="shadow-md" />
      </div>

      <Modal
        title={<h1 className="text-xl font-bold text-blue-900">THÊM GIÁO VIÊN MỚI</h1>}
        centered
        open={state.openForm}
        width={800}
        onCancel={() => dispatch({ type: "closeForm" })}
        footer={[]}>
        <CreateForm />
      </Modal>
    </Context.Provider>
  )
}

export default GiaoVienPage