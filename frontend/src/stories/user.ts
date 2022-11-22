import create from "zustand";

export const useUserStore = create((set) => ({
  user: {
    _id: { $oid: "" },
    id: 1,
    ETH: 0,
    USDT: 0,
    date_of_maturity: 0,
    priceETH: 0
  },
  fetchUser: async () => {
    const res = await fetch(`${import.meta.env.VITE_SERVER_URL}/user/1`)
      .then((res) => res.json())
    set({ user: res});
    return res;
  },
  setPriceETH: (value: any) => set((state: any) => ({ user: { ...state.user, priceETH: value}})),
  setMoney: (value: any) => set((state: any) => ({ user: { ...state.user, money_per_turn: value}})),
  setTime: (value: any) => set((state: any) => ({ user: { ...state.user, investment_time: value}})),
  setETH: (value: any) => set((state: any) => ({ user: { ...state.user, ETH: value}})),
  setUSDT: (value: any) => set((state: any) => ({ user: { ...state.user, USDT: value}})),
  setStatus: (value: boolean) => set((state: any) => ({ user: { ...state.user, status: value}})),
  setRemainingInvestmentTime: (value: boolean) => set((state: any) => ({ user: { ...state.user, remaining_investment_time: value}})),
}));
