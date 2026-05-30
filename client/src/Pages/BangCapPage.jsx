import TableHeader from "@/Components/TableHeader";
import { getNextIdNumber } from "@/Utils/FormUtils";
import { faArrowRotateRight, faCheck, faPen, faPlus, faTrash, faUpload } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button, Input, message, Modal, Popconfirm, Table } from "antd";
import axios from "axios";
import { useEffect, useRef, useState } from "react";


function BangCapPage() {
  const [messageApi, contextHolder] = message.useMessage();
  const [form, setForm] = useState({
    maBangCap: "",
    tenBangCap: "",
    tenVietTat: "",
  })
  const createFormRef = useRef();
  const [createForm, setCreateForm] = useState(false)
  const [mode, setMode] = useState('create')
  const [data, setData] = useState([])

  const success = (content) => {
    messageApi.open({ type: 'success', content });
  };

  const error = m => messageApi.open({ type: 'error', content: m, });

  const columns = [
    {
      title: <TableHeader>STT</TableHeader>,
      dataIndex: 'stt', width: 5,
      render: (_, record, index) => <TableHeader>{index + 1}</TableHeader>
    },
    {
      dataIndex: 'maBangCap', key: 'maBangCap', width: 120,
      title: () => <TableHeader>Mã bằng cấp</TableHeader>,
      render: i => <div className="text-lg text-center">{i}</div>
    },
    {
      dataIndex: 'tenBangCap', key: 'tenBangCap', width: 400,
      title: () => <TableHeader>Tên bằng cấp</TableHeader>,
      render: i => <div className="text-lg text-center">{i}</div>
    },
    {
      dataIndex: 'tenVietTat', key: 'tenVietTat', width: 120,
      title: () => <TableHeader>Tên viết tắt</TableHeader>,
      render: i => <div className="text-lg text-center">{i}</div>
    },
    {
      title: () => <TableHeader>Thao tác</TableHeader>, key: 'action', width: 100,
      render: (_, entry) => (
        <div className="flex gap-5 items-center justify-center" >
          <Button data-testid="btn-sua" title="Sửa" variant="outlined" color="blue" icon={<FontAwesomeIcon icon={faPen} />}
            onClick={async () => {
              setCreateForm(true)
              setMode("edit")
              setForm({
                maBangCap: entry.maBangCap,
                tenBangCap: entry.tenBangCap,
                tenVietTat: entry.tenVietTat,
                id: entry.id
              })
            }} />
          <Popconfirm
            title="Bạn có chắc chắn muốn xóa bằng cấp này không?"
            description="Bằng cấp này sẽ bị xóa vĩnh viễn!"
            placement="left"
            onConfirm={() => axios.delete(`http://localhost:5249/BangCap/${entry.id}`).then(() => {
              updateData()
              success("Xoá bằng cấp thành công!")
            })}>
            <Button data-testid="btn-xoa" title="Xoá" variant="outlined" color="red" icon={<FontAwesomeIcon icon={faTrash} />} />
          </Popconfirm>
        </div>
      ),
    },
  ];

  function updateData() {
    setData([])
    axios.get('http://localhost:5249/BangCap')
      .then(function (reponse) {
        setData(reponse.data.map((i, j) => ({ ...i, key: j })))
        // console.log(reponse.data)
      })
  }

  useEffect(function () {
    updateData()
  }, [])

  return (
    <>
      {contextHolder}
      <div className="p-5 flex flex-col gap-5" >
        <div className="flex justify-end gap-2 items-center">
          <Button data-testid="btn-them" variant="link" title="Thêm" color="orange" icon={<FontAwesomeIcon icon={faPlus} className="scale-150" />} onClick={() => {
            setCreateForm(true)
            setMode('create')
            setForm(d => ({ ...d, maBangCap: `BC-${getNextIdNumber(data.map(i => i.maBangCap))}` }))
          }} />
          <Button title="Upload" variant="link" color="green" icon={<FontAwesomeIcon icon={faUpload} className="scale-150" />} onClick={() => {
          }} />
          <Button title="Tải lại" variant="link" color="blue" icon={<FontAwesomeIcon icon={faArrowRotateRight} className="scale-150" />} onClick={updateData} />
        </div>

        <Table columns={columns} dataSource={data} pagination={{ pageSize: 10 }} size="small" bordered className="shadow-md" />
      </div>

      <Modal
        title={<h1 className="text-xl font-bold text-blue-900">THÊM BẰNG CẤP MỚI</h1>}
        centered
        open={createForm}
        onCancel={() => setCreateForm(false)}
        footer={[]}>
        <form
          ref={createFormRef} className="flex flex-col gap-5"
          onAbort={e => {
            console.log(e)
          }}
          onSubmit={async function (e) {
            e.preventDefault()
            const elem = e.target;
            const data = Object.fromEntries(new FormData(elem))
            if (form.tenBangCap.length === 0 || form.tenVietTat.length === 0) message.error("Nhập thiếu thông tin!")

            data.maBangCap = ""
            if (mode === 'create')
              await axios.post('http://localhost:5249/BangCap', data)
                .then(() => updateData())
                .then(success.bind({}, "Thêm bằng cấp thành công!"))
                .then(() => {
                  setForm({ maBangCap: "", tenBangCap: "", tenVietTat: "", })
                  setCreateForm(false)
                })
                .catch(res => error(res.response.data))

            else if (mode === 'edit') {
              await axios.put('http://localhost:5249/BangCap', form)
                .then(() => updateData())
                .then(success.bind({}, "Cập nhật bằng cấp thành công!"))
                .then(() => {
                  setForm({ maBangCap: "", tenBangCap: "", tenVietTat: "", })
                  setCreateForm(false)
                })
                .catch(res => error(res.response.data))
            }
          }}>
          {/* <div>
            <label className="font-semibold">Mã bằng cấp</label>
            <Input required name="maBangCap" className="pointer-events-none opacity-75" value={form.maBangCap} onChange={e => setForm(d => ({ ...d, maBangCap: e.target.value }))} />
          </div> */}
          <div>
            <label className="font-semibold">Tên bằng cấp</label>
            <Input name="tenBangCap" value={form.tenBangCap} onChange={e => setForm(d => ({ ...d, tenBangCap: e.target.value }))} />
          </div>
          <div>
            <label className="font-semibold">Tên viết tắt</label>
            <Input maxLength={10} showCount name="tenVietTat" value={form.tenVietTat} onChange={e => setForm(d => ({ ...d, tenVietTat: e.target.value }))} />
          </div>
          <Button data-testid="btn-submit" htmlType="submit" className="w-min self-end" variant="solid" color="orange" icon={<FontAwesomeIcon icon={faCheck} />}>
            Hoàn thành
          </Button>
        </form>
      </Modal >
    </>
  )
}

export default BangCapPage