import create from "zustand";

export const useHistoryStore = create((set) => ({
  list: [],
  fetchHistories: async () => {
    const res = await fetch(`${import.meta.env.VITE_SERVER_URL}/histories/1`)
      .then((res) => res.json())
    set({ list: res});
    return res;
  },
  add: (value: any) => set((state:any) => {
    const isValid = state.list.some(({ _id }) => {
      return _id.$oid === value._id.$oid
    })
    if (!isValid) return { list: [...state.list, value] }
    return state
  }) 
}));
