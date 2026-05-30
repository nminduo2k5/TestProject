import avartar from '@/assets/avartar.png'
import { Select } from 'antd'

function Topbar() {
  return (
    <div className="bg-white border-b-1 flex justify-end items-center px-5 py-2 gap-3">
      <img src={avartar} className='' />
      <p className='text-center text-sm text-gray-700'>
        Lê Văn A
        <br />
        (MU123456)
      </p>
      {/* <Select className='w-25' defaultValue="Admin" options={[
        { value: "Admin", label: "Admin" }
      ]} /> */}
    </div>
  )
}

export default Topbar