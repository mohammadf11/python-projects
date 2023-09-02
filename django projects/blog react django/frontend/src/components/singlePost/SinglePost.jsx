import { Link, useParams } from "react-router-dom";
import "./singlePost.css";
import { useNavigate } from "react-router-dom";
import {
  usePostDeleteMutation,
  usePostDetailQuery,
} from "../../services/postApi";

export default function SinglePost() {
  const navigate = useNavigate();
  const { id } = useParams();

  const { data: post } = usePostDetailQuery(id);
  const [deletePost] = usePostDeleteMutation();

  const deletePostHandler = async () => {
    const res = await deletePost(id);
    navigate("/");
  };

  const editPostHandler = () => {
    console.log(post);
    navigate("/write", { state: { initPost: post } });

  };
  return (
    <>
      {post ? (
        <div className="singlePost">
          <div className="singlePostWrapper">
            <img className="singlePostImg" src={post.photo} alt="" />
            <h1 className="singlePostTitle">
              {post.title}
              <div className="singlePostEdit">
                <i
                  className="singlePostIcon far fa-edit"
                  onClick={editPostHandler}
                ></i>
                <i
                  className="singlePostIcon far fa-trash-alt"
                  onClick={deletePostHandler}
                ></i>
              </div>
            </h1>
            <div className="singlePostInfo">
              <span>
                Author:
                <b className="singlePostAuthor">
                  <Link className="link" to="/posts?username=Safak">
                    {post.author}
                  </Link>
                </b>
              </span>
              <span>{post.updated}</span>
            </div>
            <p className="singlePostDesc">{post.body}</p>
          </div>
        </div>
      ) : (
        ""
      )}
    </>
  );
}
