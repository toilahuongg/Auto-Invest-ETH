import { Select } from "antd";
import { useState } from "react";
import { useHistoryStore } from "../../stories/history";
import StatisticChart from "./StatisticChart";
import Statistic from "./StatisticTable";

const Statistical = () => {
  const [type, setType] = useState('table')
  const { list } = useHistoryStore() as any;
  return (
    <div className="my-5 max-w-xl">
      <Select 
        value={type}
        options={[
          { label: "Bảng", value: "table"},
          { label: "Biểu đồ", value: "chart"},
        ]}
        onChange={(value) => setType(value)}
      />
      <div className="p-2">
        Tổng: {list.length} bản ghi
      </div>
      { type === 'table' ? (<Statistic />) : <StatisticChart />}
    </div>
  )
}

export default Statistical;