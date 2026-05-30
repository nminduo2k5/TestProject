import { faCheck, faX } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button, InputNumber, message, Modal, Select } from 'antd';
import { useState } from 'react';

import { CreateLopHocPhan, GetLopHocPhanList } from "@/api/lopHocPhanApi";
import { useData } from "./context";

function BulkAddModal() {
  const [{
    addBulkModal, khoaData, hocPhanData, hocKiData, namHocData, bulkForm
  }, dispatch] = useData()
  const { hocPhanId, hocKiId, soLuongSinhVien, soLop, khoaId } = bulkForm

  const [classes, setClasses] = useState([])
  const [successModal, setSuccessModal] = useState(false)

  // const [khoaId, setKhoaId] = useState()
  const [nam, setNam] = useState()

  const handleSubmit = async () => {
    if (!hocPhanId) return message.error("Nhập thiếu thông tin!")
    if (!hocKiId) return message.error("Nhập thiếu thông tin!")
    if (soLuongSinhVien <= 0) return message.error("Số lượng sinh viên phải lớn hơn 0!")

    const result = []

    for (let i = 0; i < soLop; ++i) {
      const res = await CreateLopHocPhan({ hocPhanId, hocKiId, soLuongSinhVien })
      result.push(res)
    }
    setClasses(result)
    setSuccessModal(true)

    dispatch([
      { type: 'updateAddBulkModal', payload: false },
      { type: 'updateLopHocPhanData', payload: await GetLopHocPhanList() },
      { type: 'resetBulkForm' }
    ])
  };

  return (
    <>
      <Modal open={successModal} width={600} centered footer={[]}
        onCancel={() => {
          setSuccessModal(false)
          setClasses([])
        }}
        title={<p className='text-xl font-bold uppercase text-center' style={{ color: '#0A34A0' }}>THÊM LỚP HỌC PHẦN THÀNH CÔNG!</p>}
        closeIcon={<FontAwesomeIcon icon={faX} className='scale-120 text-orange-400' />}>

        {/* Content */}
        <h3 className="text-lg font-semibold mb-4" style={{ color: '#0A34A0' }}>
          Danh sách lớp học phần vừa tạo ({classes.length}):
        </h3>

        {/* Class List */}
        <div className="space-y-3 h-100 overflow-y-auto">
          {classes.map((classItem, index) => (
            <div key={index} className="flex items-center bg-gray-50 rounded-lg p-1 hover:bg-gray-100 transition-colors" >
              <div className="border border-blue-300 rounded px-4 py-2 min-w-[120px] text-center" style={{ backgroundColor: '#E9FAFF' }}>
                <span className="text-blue-700 font-medium" >
                  {classItem.maLop}
                </span>
              </div>
              <div className="ml-4 flex-1">
                <span className="text-gray-800">
                  {classItem.tenLop} ({classItem.soLuongSinhVien} sinh viên)
                </span>
              </div>
            </div>
          ))}
        </div>
      </Modal>

      <Modal
        centered
        title={<h1 className="text-xl font-bold text-blue-900 uppercase">Tạo hàng loạt lớp học phần</h1>}
        open={addBulkModal}
        onCancel={() => {
          // setKhoaId()
          setNam()
          dispatch([
            { type: 'updateAddBulkModal', payload: false },
            { type: 'resetBulkForm' }
          ])
        }}
        footer={[
          <Button htmlType="submit" className="w-min self-end" variant="solid" color="orange" onClick={handleSubmit} key="submit">
            Hoàn thành
            {<FontAwesomeIcon icon={faCheck} />}
          </Button>
        ]}
        width={600}>
        <form className="flex flex-col gap-5">
          <div className="grid grid-cols-2 gap-5">
            <div className="flex flex-col gap-2">
              <label className="font-semibold">Khoa</label>
              <Select
                placeholder="Chọn khoa"
                value={khoaId || undefined}
                onChange={(value) => {
                  dispatch([
                    { type: 'updateBulkForm', payload: { name: 'khoaId', value } },
                    { type: 'updateBulkForm', payload: { name: 'hocPhanId' } }
                  ])
                }}
                options={khoaData.map(khoa => ({ value: khoa.id, label: khoa.tenKhoa }))} />
            </div>

            <div className="flex flex-col gap-2">
              <label className="font-semibold">Học phần</label>
              <Select
                placeholder="Chọn học phần"
                disabled={!khoaId}
                value={hocPhanId || undefined}
                onChange={(value) => dispatch([
                  { type: 'updateBulkForm', payload: { name: 'hocPhanId', value } }
                ])}
                options={hocPhanData.filter(hp => hp.khoaId == khoaId).map(hp => ({ value: hp.id, label: `${hp.maHocPhan}-${hp.tenHocPhan} (${hp.soTinChi} TC)` }))} />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-5">
            <div className="flex flex-col gap-2">
              <label className="font-semibold">Năm học</label>
              <Select
                placeholder="Chọn năm học"
                value={nam || undefined}
                onChange={(value) => {
                  setNam(value)
                  dispatch([
                    { type: 'updateBulkForm', payload: { name: 'hocKiId' } }
                  ])
                }}
                options={namHocData.map(nam => ({ value: nam.nam, label: `${nam.nam} - ${nam.nam + 1}` }))} />
            </div>

            <div className="flex flex-col gap-2">
              <label className="font-semibold">Kỳ học</label>
              <Select
                placeholder="Chọn kỳ"
                disabled={!nam}
                value={hocKiId || undefined}
                onChange={(value) => dispatch([
                  { type: 'updateBulkForm', payload: { name: 'hocKiId', value } }
                ])}
                options={hocKiData.filter(ky => new Date(ky.thoiGianBatDau).getFullYear() == nam).map(ky => ({ value: ky.id, label: ky.tenKi }))} />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-5">
            <div className="flex flex-col gap-2">
              <label className="font-semibold">Số lớp cần tạo</label>
              <InputNumber min={1} max={20} placeholder="3" style={{ width: '100%' }}
                value={soLop || undefined}
                onChange={(value) => dispatch([
                  { type: 'updateBulkForm', payload: { name: 'soLop', value } }
                ])} />
            </div>

            <div className="flex flex-col gap-2">
              <label className="font-semibold">Số sinh viên mỗi lớp</label>
              <InputNumber min={1} max={100} placeholder="45" style={{ width: '100%' }}
                value={soLuongSinhVien || undefined}
                onChange={(value) => dispatch([
                  { type: 'updateBulkForm', payload: { name: 'soLuongSinhVien', value } }
                ])} />
            </div>
          </div>
        </form>
      </Modal >
    </>
  )
}

export default BulkAddModal;