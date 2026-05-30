import { faArrowRotateRight, faPlus, faUpload } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Button, Select } from 'antd';

import { useContext, useEffect } from 'react';
import { Context } from './context';

function FunctionBar() {
  const [{
    selectedYear, yearList
  }, dispatch] = useContext(Context)

  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
        <div>
          <span style={{ marginRight: '8px', fontWeight: 'bold' }}>Năm học:</span>
          <Select className='w-40' placeholder="Chọn năm học"
            selectedYear={selectedYear}
            onChange={e => dispatch({ type: "updateSelectedYear", payload: e })}
            options={[
              { value: "all", label: "Tất cả năm học" },
              ...yearList.map(nam => ({ value: nam.nam, label: `${nam.nam}-${nam.nam + 1}` }))
            ]} />
        </div>
      </div>
      <div className="flex justify-end gap-2 items-center">
        <Button variant="link" color="orange" icon={<FontAwesomeIcon icon={faPlus} className="scale-150" />}
          onClick={() => {
            dispatch([
              { type: "updateModelMode", payload: "add" },
              { type: "updateModel", payload: true },
              { type: "resetFormData" }
            ])
          }} />
        <Button variant="link" color="green" icon={<FontAwesomeIcon icon={faUpload} className="scale-150" />}
          onClick={() => {

          }} />
        <Button variant="link" color="blue" icon={<FontAwesomeIcon icon={faArrowRotateRight} className="scale-150" />}
          onClick={() => {

          }} />
      </div>
    </div>
  )
}

export default FunctionBar