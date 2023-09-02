import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  phone_number: "",
  email: "",
  name: "",
};

export const userSlice = createSlice({
  name: "user_info",
  initialState,
  reducers: {
    setUserInfo: (state, action) => {
      state.email = action.payload.email;
      state.phone_number = action.payload.phone_number;
      state.name = action.payload.name;
    },
  },
});

export const { setUserInfo } = userSlice.actions;

export default userSlice.reducer;
