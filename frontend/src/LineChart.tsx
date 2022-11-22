import dayjs from 'dayjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
);

export const LineChart = ({ dataFetch, prop }: any) => {
  const options = {
    responsive: true,
  };
  const data = {
    labels: dataFetch.map(({ create_at }) => {
      const t = dayjs(create_at);
      return t.format('DD-MM-YYYY')
    }),
    datasets: [
      {
        label: prop,
        data: dataFetch.map(item => item[prop]) as any[],
        borderColor: "rgb(255, 99, 132)",
        backgroundColor: "rgba(255, 99, 132, 0.5)",
        borderWidth: 1,
        radius: 0
      }
    ],
  };
  
  return <Line options={options} data={data} />;
}
