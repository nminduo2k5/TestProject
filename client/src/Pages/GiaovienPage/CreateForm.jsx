import { faCheck } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { Button, DatePicker, Input, message, Radio, Select } from "antd"
import axios from "axios"
import dayjs from 'dayjs'
import { useContext, useEffect } from "react"

import { getNextIdNumber } from "@/Utils/FormUtils"
import Context from "./context"

function CreateForm() {
  const [state, dispatch] = useContext(Context)
  const [messageApi, contextHolder] = message.useMessage();
  const success = (m) => messageApi.open({ type: 'success', content: m, });
  const error = m => messageApi.open({ type: 'error', content: m, });

  useEffect(function () {
    axios.get("http://localhost:5249/BangCap")
      .then(res => dispatch({ type: "updateBangCap", payload: res.data }))
    axios.get("http://localhost:5249/Khoa")
      .then(res => dispatch({ type: "updateKhoa", payload: res.data }))
    axios.get('http://localhost:5249/ChucVu')
      .then(res => dispatch({ type: "updateChucVu", payload: res.data }))
  }, [dispatch])

  function updateData() {
    axios.get('http://localhost:5249/GiangVien')
      .then(res => {
        dispatch({ type: "updateGiangVienData", payload: res.data })
        return res.data
      }).then(res => dispatch({ type: "updateGVInput", payload: { name: "maGiangVien", value: `GV-${getNextIdNumber(res.map(i => i.maGiangVien))}` } }))
  }
  return (
    <>
      {contextHolder}
      <form className="grid gap-5 grid-cols-2"
        onSubmit={async function (e) {
          e.preventDefault()
          const { giangVien: { tenGiangVien, soDienThoai, gioiTinh, mail, bangCapId }, khoaId, chucVuId } = state.formValue
          console.log({ tenGiangVien, soDienThoai, gioiTinh, mail, bangCapId, khoaId, chucVuId })
          if (tenGiangVien.length === 0 || soDienThoai.length === 0 || mail.length === 0 || bangCapId === undefined || khoaId === undefined || chucVuId === undefined)
            return message.error("Nhập thiếu thông tin!")

          // const data = Object.fromEntries(new FormData(e.target))
          // await axios.post('http://localhost:5249/Khoa', data)
          if (state.mode === 'create') {
            await axios.post('http://localhost:5249/GiangVien/them-giang-vien', state.formValue)
              .then(() => {
                success("Thêm giáo viên thành công!")
                dispatch({ type: "resetInput" })
                dispatch({ type: "closeForm" })
                updateData()
              }).catch(err => error(`Thông tin không hợp lệ. ${err.response.data}`))

          } else if (state.mode === 'update') {
            await axios.put('http://localhost:5249/GiangVien/sua-thong-tin', state.formValue)
              .then(() => {
                success("Sửa giáo viên thành công!")
                dispatch({ type: "resetInput" })
                dispatch({ type: "closeForm" })
                updateData()
              }).catch(err => error(`Thông tin không hợp lệ. ${err.response.data}`))
          }
        }
        }>
        {/* <div>
          <label className="font-semibold">Mã giáo viên</label>
          <Input  disabled name="maGiangVien" value={state.formValue.giangVien.maGiangVien} />
        </div> */}
        <div className="">
          <label className="font-semibold">Họ tên</label>
          <Input name="tenGiangVien" value={state.formValue.giangVien.tenGiangVien}
            onChange={e => dispatch({ type: "updateGVInput", payload: { name: e.target.name, value: e.target.value } })} />
        </div>
        <div >
          <label className="font-semibold">Khoa</label>
          <br />
          <Select className="w-full" name="khoaId"
            onChange={e => dispatch({ type: "updateKhoaInput", payload: e })}
            value={state.formValue.khoaId || undefined}
            options={state.khoaData.map(i => ({ value: i.id, label: i.tenKhoa }))} />
        </div>

        <div>
          <label className="mb-5 font-semibold">Giới tính</label>
          <br />
          <Radio.Group className="w-full" name="gioiTinh" value={state.formValue.giangVien.gioiTinh}
            options={[{ value: 0, label: "Nam" }, { value: 1, label: "Nữ" }]}
            onChange={e => dispatch({ type: "updateGVInput", payload: { name: e.target.name, value: e.target.value } })} />
        </div>
        <div>
          <label className="font-semibold">Ngày sinh</label>
          <br />
          <DatePicker
            className="w-full"
            name="sinhNhat"
            value={dayjs(state.formValue?.giangVien?.sinhNhat)}
            onChange={e => dispatch({ type: "updateGVInput", payload: { name: 'sinhNhat', value: e.toDate() } })} />
          {/* <input  className="w-full border-1 rounded border-gray-300 p-1" type="date" name="sinhNhat"
            value={convertDateToInput(state.formValue.giangVien.sinhNhat)}
            onChange={e => dispatch({ type: "updateGVInput", payload: { name: e.target.name, value: parseDateFromInput(e.target.value) } })} /> */}
        </div>
        <div>
          <label className="font-semibold">Số điện thoại</label>
          <Input

            name="soDienThoai"
            value={state.formValue.giangVien.soDienThoai}
            onChange={e => dispatch({ type: "updateGVInput", payload: { name: e.target.name, value: e.target.value } })} />
        </div>
        <div>
          <label className="font-semibold">Mail</label>
          <Input

            name="mail"
            value={state.formValue.giangVien.mail}
            onChange={e => dispatch({ type: "updateGVInput", payload: { name: e.target.name, value: e.target.value } })} />
        </div>
        <div>
          <label className="font-semibold">Bằng cấp</label>
          <Select name="bangCapId" className="w-full" value={state.formValue.giangVien.bangCapId}
            options={state.bangCapData.map(i => ({ value: i.id, label: i.tenBangCap }))}
            onChange={e => dispatch({ type: "updateGVInput", payload: { name: "bangCapId", value: e } })} />
        </div>
        <div>
          <label className="font-semibold">Chức vụ</label>
          <Select className="w-full" name="chucVuId" value={state.formValue.chucVuId}
            options={state.chucVuData.map(i => ({ value: i.id, label: i.tenChucVu }))}
            onChange={e => dispatch({ type: "updateChucVuInput", payload: e })} />
        </div>
        <div className="col-span-2 flex justify-end">
          <Button data-testid="btn-submit" htmlType="submit" className="w-min" variant="solid" color="orange" icon={<FontAwesomeIcon icon={faCheck} />}>
            Hoàn thành
          </Button>
        </div>
      </form>
    </>
  )
}

export default CreateForm