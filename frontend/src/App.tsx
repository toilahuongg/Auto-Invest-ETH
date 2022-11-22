import { Tabs } from "antd";
import { useEffect, useState } from "react";
import General from "./components/General";
import Statistical from "./components/Statistical";
import { socketio } from "./socketio";
import { useHistoryStore } from "./stories/history";
import { useUserStore } from "./stories/user";

function App() {
  const user = useUserStore() as any;
  const history = useHistoryStore() as any;
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    (async () => {
      setLoading(true);
      await Promise.all([user.fetchUser(), history.fetchHistories()]);
      setLoading(false);
    })();
    socketio.on("priceETH", (price) => {
      user.setPriceETH(price);
    });
    socketio.on("update_after_market", (value) => {
      const data = JSON.parse(value);
      user.setRemainingInvestmentTime(data.remaining_investment_time);
      history.add(data.history);
      user.setETH(data.history.ETH)
      user.setUSDT(data.history.USDT)
    });
  }, []);
  return loading ? (
    "Loading ..."
  ) : (
    <div className="p-5">
      <Tabs
        items={[
          {
            label: "Tổng quan",
            key: "tong-quan",
            children: <General />,
          },
          {
            label: "Thống kê",
            key: "thong-ke",
            children: <Statistical />,
          },
          // {
          //   label: "Tin tức",
          //   key: "tin-tuc",
          // },
        ]}
      />
    </div>
  );
}

export default App;
