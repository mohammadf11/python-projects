import { useLoginUserMutation } from "../../services/userAuthApi";
import "./login.css";
import { useState } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import {
  ExpiredRefreshToken,
  storeToken,
} from "../../services/LocalStorageService";
import { setUserToken } from "../../features/authSlice";
import { ExpiredToken } from "../../services/LocalStorageService";

export default function Login() {
  const [login, { isloading }] = useLoginUserMutation();
  const [server_error, setServerError] = useState({});
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const submitHandler = async (e) => {
    e.preventDefault();
    const data = new FormData(e.currentTarget);
    const userData = {
      phone_number: data.get("phone_number"),
      password: data.get("password"),
    };
    const res = await login(userData);
    if (res.error) {
      console.log(res);
      setServerError(res.error.data);
    }
    if (res.data) {
      console.log(res);
      storeToken(res.data.token);
      dispatch(
        setUserToken({
          access_token: res.data.token["access"],
        })
      );
      ExpiredToken(dispatch);
      ExpiredRefreshToken(dispatch);

      navigate("/");
    }
  };
  return (
    <div className="login">
      <span className="loginTitle">Login</span>
      <form className="loginForm" onSubmit={submitHandler}>
        <label>Phone Number</label>
        <input
          className="loginInput"
          type="text"
          name="phone_number"
          placeholder="Enter your Phone Number..."
        />
        <label>Password</label>
        <input
          className="loginInput"
          type="password"
          name="password"
          placeholder="Enter your password..."
        />
        <button type="submit" className="loginButton">
          Login
        </button>
      </form>
      <button className="loginRegisterButton">Register</button>
    </div>
  );
}
