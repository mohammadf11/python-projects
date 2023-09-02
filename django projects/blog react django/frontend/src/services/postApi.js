import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { getToken } from './LocalStorageService';

export const postApi = createApi({
    reducerPath: 'api',
    tagTypes: ['Post'],
    baseQuery: fetchBaseQuery({
        baseUrl: 'http://127.0.0.1:8000/api/posts/',
        prepareHeaders: (headers) => {
            const token = getToken().access_token;
            
            if (token) {
                headers.set('Authorization', `Bearer ${token}`)
            }
            return headers
        },
    }),
    endpoints: (builder) => ({
        postList: builder.query({
            query: () => '',
            providesTags: (result, error, arg) =>
                result
                    ? [
                        ...result.map(({ id }) => ({ type: "Post", id })),
                        "Post",
                    ]
                    : ["Post"],


        }),
        postDetail: builder.query({
            query: (id) => `${id}/`,
            providesTags: ['Post']
            // providesTags: (result, error, arg) => [{ type: "Project", id: arg}]
        }),
        postCreate: builder.mutation({
            query: (data) => ({
                url: ``,
                method: "POST",
                body: data,
            }),
            invalidatesTags: ['Post'],

        }),
        postUpdate: builder.mutation({
            query: ({ id, data }) => ({
                url: `${id}/`,
                method: "PATCH",
                body: data
            }),
            invalidatesTags: ['Post'],
            //   invalidatesTags: (result, error, arg) => [
            //     {type: 'Project', id: arg}
            //   ]
        }),

        postDelete: builder.mutation({
            query: (id) => ({
                url: `${id}/`,
                method: "DELETE",
            }),
            invalidatesTags: ['Post'],
            //   invalidatesTags: (result, error, arg) => [
            //     { type: "Project", id: arg },
            // ],
        })
    }),
});

export const { usePostListQuery, usePostDetailQuery, useAddProjectMutation, usePostUpdateMutation, usePostDeleteMutation, usePostCreateMutation } = postApi;