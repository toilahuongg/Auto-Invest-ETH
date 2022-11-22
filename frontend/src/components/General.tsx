import { Button, Form, Input, Select } from "antd";
import { useState } from "react";
import { formatter } from "../helpers/common";
import { useUserStore } from "../stories/user";

const General = () => {
  const { user, setStatus, setMoney, setTime, setRemainingInvestmentTime } = useUserStore() as any;
  const [loading, setLoading] = useState(false);

  const handleInvest = async () => {
    setLoading(true);
    await fetch(
      `${import.meta.env.VITE_SERVER_URL}/user/${user.id}/invest`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          money: user.money_per_turn,
          time: user.investment_time,
        }),
      }
    ).then((res) => res.json());
    setStatus(true);
    setRemainingInvestmentTime(user.investment_time)
    setLoading(false);
  };

  const handleStopInvesting = async () => {
    setLoading(true);
    await fetch(
      `${import.meta.env.VITE_SERVER_URL}/user/${user.id}/stop-investing`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        }
      }
    ).then((res) => res.json());
    setStatus(false);
    setLoading(false);
  }
  return (
    <div className="my-5 max-w-lg">
      <div>
        <span className="font-bold">Fullname: </span> {user.fullname}
      </div>
      <div>
        <span className="font-bold">USDT: </span> {formatter.format(user.USDT)}
      </div>
      <div>
        <span className="font-bold">ETH: </span> {user.ETH}
      </div>
      <div>
        <span className="font-bold">Total USDT: </span>
        {formatter.format(user.ETH * user.priceETH + user.USDT)}
      </div>
      <div>
        <span className="font-bold">Trạng thái: </span>
        {user.status ? "Đang đầu tư" : "Chưa đầu tư"}
      </div>
      {user.status && (
        <div>
          <span className="font-bold">Thời gian đầu tư còn lại: </span>
          {user.remaining_investment_time} ngày
        </div>
      )}
      <div className="mt-5">
        {user.status ? (
          <Button type="default" onClick={handleStopInvesting} loading={loading}>Dừng đầu tư</Button>
        ) : (
          <Form layout="vertical">
            <Form.Item label="Số tiền đầu tư định kỳ">
              <Input
                type="number"
                value={user.money_per_turn}
                onChange={(e) => setMoney(+e.target.value)}
                min={10}
                suffix="$"
              />
            </Form.Item>
            <Form.Item label="Thời gian đầu tư định kỳ">
              <Select
                value={user.investment_time}
                options={[
                  { label: "1 tháng", value: 30 },
                  { label: "3 tháng", value: 90 },
                  { label: "6 tháng", value: 180 },
                  { label: "12 tháng", value: 365 },
                ]}
                onChange={(value) => setTime(value)}
              />
            </Form.Item>
            <Form.Item>
              <Button type="primary" onClick={handleInvest} loading={loading}>
                Đầu tư
              </Button>
            </Form.Item>
          </Form>
        )}
      </div>
    </div>
  );
};
export default General;
