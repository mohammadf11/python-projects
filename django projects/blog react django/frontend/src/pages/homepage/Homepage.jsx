import Header from "../../components/header/Header";
import Sidebar from "../../components/sidebar/Sidebar";
import "./homepage.css";
import Post from "../../components/post/Post";
import { usePostListQuery } from "../../services/postApi";
import { useState } from "react";
import { skipToken } from "@reduxjs/toolkit/dist/query";

export default function Homepage() {
  const { data: postList } = usePostListQuery();

  return (
    <>
      <Header />
      <div className="home">
        <div className="posts">
          {postList
            ? postList.map((post) => <Post post={post} key={post.id} />)
            : "No DAta"}
        </div>
        <Sidebar />
      </div>
    </>
  );
}
