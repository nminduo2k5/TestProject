import { faArrowRotateRight, faCheck, faPen, faPlus, faSearch, faTrash, faUpload } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button, Input, message, Modal, Popconfirm, Table } from "antd";
import axios from "axios";
import { useEffect, useRef, useState } from "react";

import TableHeader from "@/Components/TableHeader";
import { getNextIdNumber } from "@/Utils/FormUtils";

function KhoaPage() {
  const [messageApi, contextHolder] = message.useMessage();
  const createFormRef = useRef();
  const [search, setSearch] = useState("")
  const [createForm, setCreateForm] = useState(false)
  const [form, setForm] = useState({ maKhoa: "", tenKhoa: "", viTri: "", tenVietTat: "", moTa: "" })
  const [mode, setMode] = useState("create")
  const [data, setData] = useState([]);

  const success = m => messageApi.open({ type: 'success', content: m, });
  const error = m => messageApi.open({ type: 'error', content: m, });

  const { current: columns } = useRef([
    { title: <TableHeader>STT</TableHeader>, dataIndex: 'stt', width: 50, render: (_, record, index) => <TableHeader>{index + 1}</TableHeader> },
    { title: <TableHeader>Mã khoa</TableHeader>, dataIndex: 'maKhoa', key: 'maKhoa', width: 70, render: i => <div className="text-lg text-center">{i}</div> },
    { title: <TableHeader>Tên khoa</TableHeader>, dataIndex: 'tenKhoa', key: 'tenKhoa', width: 120, render: i => <div className="text-lg">{i}</div> },
    { title: <TableHeader>Vị trí</TableHeader>, dataIndex: 'viTri', key: 'viTri', width: 150, render: i => <div className="text-lg">{i}</div> },
    { title: <TableHeader>Mô tả</TableHeader>, dataIndex: 'moTa', key: 'moTa', width: 100, render: i => <div className="text-lg">{i}</div> },
    { title: <TableHeader>Tên viết tắt</TableHeader>, dataIndex: 'tenVietTat', key: 'tenVietTat', width: 80, render: i => <div className="text-lg text-center">{i}</div> },
    {
      title: <TableHeader>Tùy chọn</TableHeader>, key: 'action', width: 20,
      render: (_, entry) => (
        <div className="flex gap-5 items-center justify-center" >
          <Button variant="outlined" color="blue" data-testid="btn-sua"
            disabled={entry.soGiangVien > 0 || entry.soLop > 0}
            icon={<FontAwesomeIcon icon={faPen} />}
            onClick={function () {
              setMode("update")
              setCreateForm(true)
              setForm({
                maKhoa: entry.maKhoa,
                tenKhoa: entry.tenKhoa,
                viTri: entry.viTri,
                tenVietTat: entry.tenVietTat,
                id: entry.id,
                moTa: entry.moTa
              })
            }} />
          <Popconfirm title="Bạn có chắc chắn muốn xóa khoa này không?" description="Khoa này sẽ bị xóa vĩnh viễn!"
            placement="left"
            onConfirm={() => axios.delete(`http://localhost:5249/Khoa/${entry.id}`).then(() => {
              updateData()
              success("Xoá khoa thành công!")
            })}>
            <Button data-testid="btn-xoa" variant="outlined" color="red" icon={<FontAwesomeIcon icon={faTrash} />} />
          </Popconfirm>
        </div>
      ),
    },
  ]);

  async function updateData() {
    setData([])
    const response = await axios.get("http://localhost:5249/Khoa")
    setData(response.data.map((i, j) => ({ ...i, key: j })))
  }

  useEffect(function () {
    updateData()
  }, [])

  return (
    <>
      {contextHolder}
      <div className="p-5 flex flex-col gap-5" >
        <div className="flex justify-end gap-2 items-center">
          <Input placeholder="Tìm kiếm" style={{ width: "200px" }} value={search} onChange={e => setSearch(e.target.value)} />
          <Button data-testid="btn-tim" variant="link" color="blue" icon={<FontAwesomeIcon icon={faSearch} className="scale-150" />} onClick={async () => {
            const response = await axios.get("http://localhost:5249/Khoa")
            const result = response.data.filter(i => JSON.stringify(i).toLowerCase().includes(search.toLowerCase()))
            if (result.length === 0) error("Không tìm thấy kết quả!!")
            setData(result)
          }} />
          <Button data-testid="btn-them" variant="link" color="orange" icon={<FontAwesomeIcon icon={faPlus} className="scale-150" />} onClick={() => {
            setMode("create")
            setForm(d => ({ ...d, maKhoa: `K-${getNextIdNumber(data.map(i => i.maKhoa))}` }))
            setCreateForm(true)
          }} />
          <Button variant="link" color="green" icon={<FontAwesomeIcon icon={faUpload} className="scale-150" />} />
          <Button variant="link" color="blue" icon={<FontAwesomeIcon icon={faArrowRotateRight} className="scale-150" />} onClick={updateData} />
        </div>

        <Table columns={columns} dataSource={data}
          pagination={{ pageSize: 10 }} size="small" bordered className="shadow-md" />
      </div>

      <Modal centered open={createForm}
        onCancel={() => {
          setForm({ maKhoa: "", tenKhoa: "", viTri: "", tenVietTat: "", moTa: "" })
          setCreateForm(false)
        }} footer={[]}
        title={<h1 className="text-xl font-bold text-blue-900">THÊM KHOA MỚI</h1>}>
        <form ref={createFormRef} className="flex flex-col gap-5"
          onSubmit={async function (e) {
            e.preventDefault()
            if (form.tenKhoa.length === 0 || form.tenVietTat.length === 0 || form.viTri.length === 0 || form.moTa.length === 0)
              return message.error("Nhập thiếu thông tin!")

            const data = Object.fromEntries(new FormData(createFormRef.current))
            data.maKhoa = ""
            if (mode === 'create') {
              await axios.post('http://localhost:5249/Khoa', data)
                .then(async () => {
                  success("Thêm khoa thành công!")
                  await updateData()
                  setCreateForm(false)
                  setForm({ maKhoa: "", tenKhoa: "", viTri: "", tenVietTat: "" })
                })
                .catch(err => error(`Thêm khoa thất bại! ${err.response.data}`))
            }
            else if (mode === 'update') {
              await axios.put('http://localhost:5249/Khoa', form)
                .then(async () => {
                  success("Cập nhật thông tin Khoa thành công!")
                  await updateData()
                  setCreateForm(false)
                  setForm({ maKhoa: "", tenKhoa: "", viTri: "", tenVietTat: "" })
                }).catch(err => error(`Sửa khoa thất bại! ${err.response.data}`))
            }
          }}>
          {/* <div>
            <label className="font-semibold">Mã khoa</label>
            <Input required name="maKhoa" className="pointer-events-none opacity-75" value={form.maKhoa} />
          </div> */}
          <div>
            <label className="font-semibold">Tên khoa</label>
            <Input name="tenKhoa" value={form.tenKhoa} onChange={e => setForm(d => ({ ...d, tenKhoa: e.target.value }))} />
          </div>
          <div>
            <label className="font-semibold">Vị trí</label>
            <Input name="viTri" value={form.viTri} onChange={e => setForm(d => ({ ...d, viTri: e.target.value }))} />
          </div>
          <div>
            <label className="font-semibold">Tên viết tắt</label>
            <Input maxLength={10} showCount name="tenVietTat" value={form.tenVietTat} onChange={e => setForm(d => ({ ...d, tenVietTat: e.target.value }))} />
          </div>
          <div>
            <label className="font-semibold">Mô tả</label>
            <Input name="moTa" value={form.moTa} onChange={e => setForm(d => ({ ...d, moTa: e.target.value }))} />
          </div>
          <Button data-testid="btn-submit" htmlType="submit" className="w-min self-end" variant="solid" color="orange" icon={<FontAwesomeIcon icon={faCheck} />}>
            Hoàn thành
          </Button>
        </form>
      </Modal>
    </>
  )
}

export default KhoaPage