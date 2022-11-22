import { LineChart } from "../../LineChart";
import { useHistoryStore } from "../../stories/history";


const StatisticChart = () => {
  const { list } = useHistoryStore() as any;
  return (<>
    <LineChart dataFetch={list} prop="ETH" />
    <LineChart dataFetch={list} prop="USDT" />
    <LineChart dataFetch={list} prop="Total" />
  </>)
}

export default StatisticChart;