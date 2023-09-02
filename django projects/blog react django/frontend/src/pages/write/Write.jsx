import "./write.css";
import { useState } from "react";
import {
  usePostCreateMutation,
  usePostUpdateMutation,
} from "../../services/postApi";
import { useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";

export default function Write() {
  const location = useLocation();
  const initPost = location.state ? location.state.initPost : undefined;
  const [photo, setPhoto] = useState(initPost ? initPost.photo : null);
  const [title, setTitle] = useState(initPost ? initPost.title : "");
  const [body, setBody] = useState(initPost ? initPost.body : "");
  const [serverError, setServerError] = useState("");

  const [postCreate] = usePostCreateMutation();
  const [postUpdate] = usePostUpdateMutation();
  const navigate = useNavigate();

  const clearData = () => {
    setPhoto(null);
    setTitle("");
    setBody("");
  };
  const getPhoto = () => {
    if (initPost && initPost.photo === photo) return photo;
    if (photo !== null) return URL.createObjectURL(photo);
    return null;;;
  };
  const postCreateHandler = async (e) => {
    e.preventDefault();
    let formData = new FormData();
    formData.append("author", 1);
    if (initPost) {
      if (initPost.photo !== photo) formData.append("photo", photo);
    } else formData.append("photo", photo);

    formData.append("title", title);
    formData.append("body", body);
    let res;
    if (initPost) res = await postUpdate({ id: initPost.id, data: formData });
    else res = await postCreate(formData);

    if (res.error) {
      const errors = res.error.data;
      for (const error in errors) {
        if (error === "title") setTitle(errors[error]);
        if (error === "body") setBody(errors[error]);
      }
    }
    if (res.data) {
      clearData();
      navigate("/");
    }
  };

  return (
    <div className="write">
      {getPhoto && <img className="writeImg" src={getPhoto()} alt="" />}
      <form className="writeForm" onSubmit={postCreateHandler}>
        {serverError.title ? (
          <div className="error">
            <span>{serverError.title[0]}</span>
          </div>
        ) : (
          ""
        )}
        <div className="writeFormGroup">
          <label htmlFor="fileInput">
            <i className="writeIcon fas fa-plus"></i>
          </label>
          <input
            id="fileInput"
            onChange={(e) => {
              setPhoto(e.target.files[0]);
            }}
            type="file"
            style={{ display: "none" }}
          />

          <input
            className="writeInput"
            placeholder="Title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            autoFocus={true}
          />
        </div>
        {serverError.body ? (
          <div className="error">
            <span>{serverError.body[0]}</span>
          </div>
        ) : (
          ""
        )}
        <div className="writeFormGroup">
          <textarea
            className="writeInput writeText"
            placeholder="Tell your story..."
            type="text"
            value={body}
            onChange={(e) => setBody(e.target.value)}
            autoFocus={true}
          />
        </div>
        <button className="writeSubmit" type="submit">
          Publish
        </button>
      </form>
    </div>
  );
}
