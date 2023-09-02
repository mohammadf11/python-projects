import { configureStore } from '@reduxjs/toolkit'
import { setupListeners } from '@reduxjs/toolkit/query'
import { userAuthApi } from '../services/userAuthApi'
import authReducer from '../features/authSlice'
import userReducer from '../features/userSlice'
import  postReducer  from '../features/postSlice'
import { postApi } from '../services/postApi'
export const store = configureStore({
  reducer: {
    [postApi.reducerPath]: postApi.reducer,
    [userAuthApi.reducerPath]: userAuthApi.reducer,
    auth: authReducer,
    user: userReducer,
    post: postReducer

  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(userAuthApi.middleware, postApi.middleware),
})

setupListeners(store.dispatch)