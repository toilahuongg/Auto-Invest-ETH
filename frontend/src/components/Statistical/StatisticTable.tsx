import { Table } from "antd";
import { formatter } from "../../helpers/common";
import { useHistoryStore } from "../../stories/history";

const Statistic = () => {
  const { list } = useHistoryStore() as any;
  const data = list.map((item: any) => ({
    ...item,
    key: item._id.$oid,
    USDT: formatter.format(item.USDT),
    Total: formatter.format(item.Total),
  }));
  return (
    <Table
      dataSource={data}
      columns={[
        { title: "Ngày mua", key: "create_at", dataIndex: "create_at" },
        { title: "ETH", key: "ETH", dataIndex: "ETH" },
        { title: "USDT", key: "USDT", dataIndex: "USDT" },
        { title: "Total USDT", key: "Total", dataIndex: "Total" },
      ]}
    />
  );
};

export default Statistic;
