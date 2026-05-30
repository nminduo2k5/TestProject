import { faCheck } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Button, DatePicker, Input, message, Modal, Select } from 'antd';
import dayjs from 'dayjs';

import { CreateHocKy, GetHocKyList, UpdateHocKy } from '@/api/hocKiApi';
import { useData } from './context';

const { RangePicker } = DatePicker;

function isValidString(str) {
  // Chỉ cho phép chữ cái và số, KHÔNG chứa ký tự đặc biệt
  return /^[a-zA-Z0-9 ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáạảãăắẳặằâấầậẫèéẻẽẹêềễệếìíịỉòóõỏôổỗộồốùúụủũđĩơởờớỡừứửựƯĂÊÔƯƠâêôơưĂÂÊÔƯ\s\-_]+$/.test(str);
}


function DataForm() {
  const [
    { showModal, modelMode, formData, kyData },
    dispatch] = useData();
  const { id, tenKi, year, thoiGianBatDau, thoiGianKetThuc } = formData
  console.log(kyData)
  //   {
  //     "tenKi": "3e231b1a-0c9a-4ca1-8891-12bd8fc6b5b1",
  //     "thoiGianBatDau": "2013-08-12T23:08:47.655Z",
  //     "thoiGianKetThuc": "2014-02-12T23:08:47.655Z",
  //     "id": "166faae4-0c7c-452c-99e7-cec827a9b2ea",
  //     "soLop": 42,
  //     "key": 109
  // }
  async function onSubmit() {
    // console.log(thoiGianBatDau, thoiGianKetThuc)

    if (!thoiGianBatDau) return message.error("Nhập thiếu thông tin!")
    if (!thoiGianKetThuc) return message.error("Nhập thiếu thông tin!")
    if (!tenKi) return message.error("Nhập thiếu thông tin!")
    if (thoiGianKetThuc.diff(thoiGianBatDau, 'month') < 4) return message.error("Thời gian kết thúc phải cách thời gian bắt đầu 4 tháng!")
    // const _bd = thoiGianBatDau.toDate(), _kt = thoiGianKetThuc.toDate();
    if (!isValidString(tenKi)) return message.error("Tên học kì không được chứa kí tự đặc biệt (ngoại trừ dấu - và _ )!")
    if (kyData.find(i => i.tenKi === tenKi && thoiGianBatDau.year() === dayjs(i.thoiGianBatDau).year()))
      return message.error(`Học kì này đã tồn tại trong năm học ${year}-${year + 1} rồi!`)
    let result;
    try {
      if (modelMode == 'add') {
        result = await CreateHocKy({
          tenKi,
          thoiGianBatDau: thoiGianBatDau.toDate(),
          thoiGianKetThuc: thoiGianKetThuc.toDate()
        }).then(async res => {

          message.success("Thêm học kì thành công!")
          const data = await GetHocKyList()
          dispatch([
            { type: "updateModel", payload: false },
            { type: "resetFormData" },
            { type: "updateModelMode" },
            { type: "updateKyData", payload: data },
            { type: "updateSelectedYear", payload: 'all' }
          ])
        }).catch(err => {
          message.error("Lỗi không thể thêm học kì!")
        })
      }
      else if (modelMode == 'edit') {
        await UpdateHocKy({
          id: id,
          tenKi,
          thoiGianBatDau: thoiGianBatDau.toDate(),
          thoiGianKetThuc: thoiGianKetThuc.toDate()
        }).then(async vres => {
          message.success("Cập nhật học kì thành công!")
          const data = await GetHocKyList()
          dispatch([
            { type: "updateModel", payload: false },
            { type: "resetFormData" },
            { type: "updateModelMode" },
            { type: "updateKyData", payload: data },
            { type: "updateSelectedYear", payload: 'all' }
          ])
        }).catch(err => {
          message.error("Lỗi không thể sửa học kì!")
        })
      }
    }
    catch (error) {
      console.log(error)
      message.error("Lỗi không thể thêm/sửa học kì!")
    }
    // console.log(result)
    // console.log({ id, tenKi, thoiGianBatDau, thoiGianKetThuc })

  }

  return (
    <Modal open={showModal} centered width={600} title={
      <h1 className="text-xl font-bold text-blue-900 uppercase">
        {modelMode == 'edit' ? 'Sửa học kì' : 'Thêm học kì mới'}
      </h1>}
      onCancel={() => dispatch([
        { type: "updateModel", payload: false },
        { type: "resetFormData" },
        { type: "updateModelMode" }
      ])}
      footer={[
        <Button htmlType="submit" className="w-min self-end" variant="solid" color="orange" icon={<FontAwesomeIcon icon={faCheck} />}
          onClick={onSubmit}>
          Hoàn thành
        </Button>
      ]}>
      <form className='flex flex-col gap-5' initialValues={{ trangThai: 'Chưa bắt đầu' }}>
        <div className='grid gap-2' key="namHoc" name="namHoc" label="Năm học" rules={[{ required: true, message: 'Vui lòng chọn năm học!' }]}>
          <label className='font-semibold'>Năm học</label>
          <Select
            placeholder="Chọn năm học"
            required
            value={year || undefined}
            options={new Array(5)
              .fill()
              .map((_, i) => {
                const nam = new Date().getFullYear() + i;
                return { value: nam, label: `${nam}-${nam + 1}` }
              })}
            onChange={e => dispatch([
              { type: "updateFormData", payload: { name: "year", value: e } }
            ])} />
        </div>
        <div className='grid gap-2' rules={[{ required: true, message: 'Vui lòng chọn thời gian!' }]}>
          <label className='font-semibold'>Thời gian</label>
          <RangePicker className="w-full" format="DD/MM/YYYY" placeholder={['Ngày bắt đầu', 'Ngày kết thúc']} required
            disabledDate={(current) => current <= new Date(year, 0, 1) || current > new Date(year + 1, 11, 31)}
            value={[thoiGianBatDau, thoiGianKetThuc]}
            onChange={e => {
              const start = e[0];
              const end = e[1];
              dispatch([
                { type: "updateFormData", payload: { name: "thoiGianBatDau", value: start } },
                { type: "updateFormData", payload: { name: "thoiGianKetThuc", value: end } },
              ])
            }} />
        </div>
        <div className='grid gap-2' >
          <label className='font-semibold'>Tên học kỳ</label>
          <Input
            placeholder="Nhập tên học kỳ"
            value={tenKi}
            required
            onChange={e => {
              dispatch({ type: "updateFormData", payload: { name: "tenKi", value: e.target.value } })
            }} />
        </div>
      </form>
    </Modal>
  )
}

export default DataForm