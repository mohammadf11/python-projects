import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    postList: [],
    psotDetail: {}
}

export const postSlice = createSlice({
    name: "post_all",
    initialState,
    reducers: {
        setPostList: (state, action) => {
            state.postList = action.payload.postList
        },
        setPostDetail: (state, action) => {
            state.psotDetail = action.payload.psotDetail
        }
    }

})


export const { setPostList, setPostDetail } = postSlice.actions;
export default postSlice.reducer;
