import { Link } from "react-router-dom";
import "./post.css";
import { useNavigate } from 'react-router-dom';

export default function Post({ post }) {
  const navigate = useNavigate();

  const postDetailLink = () => {
    navigate(`/post/${post.id}`);
  };
  return (
    <div className="post" onClick={postDetailLink}>
      <img className="postImg" src={post.photo} alt="" />
      <div className="postInfo">
        <div className="postCats">
          <span className="postCat">
            <Link className="link" to="/posts?cat=Music">
              Music
            </Link>
          </span>
          <span className="postCat">
            <Link className="link" to="/posts?cat=Music">
              Life
            </Link>
          </span>
        </div>
        <span className="postTitle">{post.title}</span>
        <hr />
        <span className="postDate">1 hour ago</span>
      </div>
      <p className="postDesc">{post.body}</p>
    </div>
  );
}
