import { faCheck } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button, InputNumber, Modal, Select, message } from 'antd';

import { CreateLopHocPhan, GetLopHocPhanList, UpdateLopHocPhan } from '@/api/lopHocPhanApi';
import { useData } from './context';

function FormModal() {
  const [messageApi, contextHolder] = message.useMessage()
  const [{
    addModal, khoaData, hocPhanData, hocKiData, namHocData, form, formMode
  }, dispatch] = useData()
  const { hocPhanId, hocKiId, giangVienId, soLuongSinhVien, khoaId, nam, id } = form;

  const handleSubmit = async () => {
    if (!hocPhanId) return message.error("Nhập thiếu thông tin!")
    if (!hocKiId) return message.error("Nhập thiếu thông tin!")
    if (soLuongSinhVien <= 0) return message.error("Số lượng sinh viên phải lớn hơn 0!")
    if (!id && formMode == 'edit') return message.error("Sửa học phần thất bại!")

    let result;
    if (formMode == 'add') {
      result = await CreateLopHocPhan({ hocPhanId, hocKiId, giangVienId, soLuongSinhVien })
      messageApi.success(`Thêm thành công ${result?.tenLop}`)
    }
    else {
      result = await UpdateLopHocPhan({ hocPhanId, hocKiId, giangVienId, soLuongSinhVien, id })
      messageApi.success(`Sửa thành công ${result?.tenLop}`)
    }
    dispatch([
      { type: "updateAddModal", payload: false },
      { type: "updateLopHocPhanData", payload: await GetLopHocPhanList() },
      { type: 'resetForm' }
    ])
  };
  return (
    <>
      {contextHolder}
      <Modal
        centered
        open={addModal}
        width={600}
        title={<h1 className="text-xl font-bold text-blue-900 uppercase">
          {formMode == 'edit' ? 'Sửa lớp học phần' : 'Thêm lớp học phần mới'}
        </h1>}
        onCancel={() => dispatch([
          { type: "updateAddModal", payload: false },
          { type: 'resetForm' }
        ])}
        footer={[
          <Button htmlType="submit" className="w-min self-end" variant="solid" color="orange"
            onClick={handleSubmit} key="submit">
            Hoàn thành
            {<FontAwesomeIcon icon={faCheck} />}
          </Button>
        ]}>
        <form className="my-5" layout="vertical" onFinish={handleSubmit}>
          <div className="grid-cols-2 grid gap-x-5 gap-y-5 mb-5 w-full">
            <div className=" flex flex-col gap-2" name="khoa">
              <label className="font-semibold">Khoa</label>
              <Select
                // className="w-35"
                placeholder="Chọn khoa"
                value={khoaId || undefined}
                onChange={a => dispatch([
                  { type: "updateForm", payload: { name: 'khoaId', value: a } },
                  { type: "updateForm", payload: { name: 'hocPhanId' } }
                ])}
                options={khoaData.map(khoa => ({ value: khoa.id, label: khoa.tenKhoa }))} />
            </div>
            <div className=" flex flex-col gap-2">
              <label className="font-semibold">Học phần</label>
              <Select
                // styles={{ width: "100%" }}
                placeholder="Chọn học phần"
                disabled={!khoaId}
                value={hocPhanId || undefined}
                onChange={a => dispatch([{ type: "updateForm", payload: { name: 'hocPhanId', value: a } }])}
                options={hocPhanData
                  .filter(hp => hp.khoaId == khoaId)
                  .map(hp => ({ value: hp.id, label: `${hp.maHocPhan}-${hp.tenHocPhan} (${hp.soTinChi} TC)` }))} />
            </div>
            {/* </div>
          <div className="grid-cols-2 grid gap-10 mb-5 w-full"> */}
            <div className="flex flex-col gap-2" >
              <label className="font-semibold">Năm học</label>
              <Select
                placeholder="Chọn năm học"
                value={nam || undefined}
                onChange={a => dispatch([
                  { type: "updateForm", payload: { name: 'nam', value: a } },
                  { type: "updateForm", payload: { name: 'hocKiId' } }
                ])}
                options={namHocData
                  .filter(ky => {
                    // console.log(ky)
                    return ky.nam >= new Date().getFullYear()
                  })
                  .map(nam => ({ value: nam.nam, label: `${nam.nam} - ${nam.nam + 1}` }))} />
            </div>
            <div className="flex flex-col gap-y-2" >
              <label className="font-semibold">Kỳ học</label>
              <Select
                placeholder="Chọn kỳ"
                disabled={!nam}
                value={hocKiId || undefined}
                onChange={a => dispatch([
                  { type: "updateForm", payload: { name: 'hocKiId', value: a } }
                ])}
                options={hocKiData
                  .filter(ky => new Date(ky.thoiGianBatDau).getFullYear() == nam)
                  .map(ky => ({ value: ky.id, label: ky.tenKi }))} />
            </div>
            <div className="flex flex-col gap-2" >
              <label className="font-semibold">Số sinh viên</label>
              <InputNumber min={1} max={100} placeholder="45"
                value={soLuongSinhVien || undefined}
                style={{ width: "100%" }}
                onChange={a => dispatch([
                  { type: "updateForm", payload: { name: 'soLuongSinhVien', value: a } }
                ])} />
            </div>
          </div>

        </form>
      </Modal>
    </>
  )
}

export default FormModal;