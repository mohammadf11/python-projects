import { useState } from "react";
import { ExpiredRefreshToken, storeToken } from "../../services/LocalStorageService.js";
import {
  useRegisterUserMutation,
  useValidInfoMutation,
} from "../../services/userAuthApi.js";
import "./register.css";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { setUserToken } from "../../features/authSlice.js";
import { ExpiredToken } from "../../services/LocalStorageService";
export default function Register() {
  const [server_error, setServerError] = useState({});
  const [verifyCode, setVerifyCode] = useState("");
  const [verifyCodeDisplay, setVerifyCodeDisplay] = useState(false);
  const [userInfo, setUserInfo] = useState({
    name: "",
    phone_number: "",
    email: "",
    password: "",
    password2: "",
    code: 0,
  });
  const navigate = useNavigate();
  const [registerUser, { isLoading }] = useRegisterUserMutation();
  const [validInfo, { Loading }] = useValidInfoMutation();
  const dispatch = useDispatch();
  const validationHandler = async (e) => {
    e.preventDefault();
    const data = new FormData(e.currentTarget);
    const userData = {
      ...userInfo,
      phone_number: data.get("phone_number"),
      name: data.get("name"),
      email: data.get("email"),
      password: data.get("password"),
      password2: data.get("password2"),
      code: 0,
    };
    setUserInfo(userData);
    const res = await validInfo(userData);
    console.log(res);
    if (res.error) {
      setServerError(res.error.data.errors);
    }
    if (res.data) {
      setVerifyCodeDisplay(true);
    }
  };
  const registerHandler = async (e) => {
    e.preventDefault();
    const userData = {
      ...userInfo,
      code: verifyCode,
    };
    const res = await registerUser(userData);
    console.log(res);
    if (res.error) {
      setServerError(res.error.data.errors);
    }
    if (res.data) {
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
    <>
      {verifyCodeDisplay ? (
        <>
          <div className="register">
            <form className="registerForm" onSubmit={registerHandler}>
              <label>Verify Code</label>
              <input
                className="registerInput"
                type="text"
                value={verifyCode}
                onChange={(e) => setVerifyCode(e.target.value)}
                placeholder="Enter your username..."
              />
              {server_error.code ? (
                <span style={{ fontSize: 12, color: "red", paddingTop: 10 }}>
                  {server_error.code[0]}
                </span>
              ) : (
                ""
              )}
              <button type="submit" className="registerButton">
                verify
              </button>
              {server_error.non_field_errors ? (
                <span severity="error">{server_error.non_field_errors[0]}</span>
              ) : (
                ""
              )}
            </form>
          </div>
        </>
      ) : (
        <div className="register">
          <span className="registerTitle">Register</span>
          <form className="registerForm" onSubmit={validationHandler}>
            <label>name</label>
            <input
              className="registerInput"
              type="text"
              name="name"
              placeholder="Enter your username..."
            />
            {server_error.name ? (
              <span style={{ fontSize: 12, color: "red", paddingTop: 10 }}>
                {server_error.name[0]}
              </span>
            ) : (
              ""
            )}
            <label>Email</label>
            <input
              className="registerInput"
              type="text"
              name="email"
              placeholder="Enter your email..."
            />
            {server_error.email ? (
              <span style={{ fontSize: 12, color: "red", paddingTop: 10 }}>
                {server_error.email[0]}
              </span>
            ) : (
              ""
            )}
            <label>Phone Number</label>
            <input
              className="registerInput"
              type="text"
              name="phone_number"
              placeholder="Enter your Phone Number..."
            />
            {server_error.phone_number ? (
              <span style={{ fontSize: 12, color: "red", paddingTop: 10 }}>
                {server_error.phone_number[0]}
              </span>
            ) : (
              ""
            )}
            <label>Password</label>
            <input
              className="registerInput"
              type="password"
              name="password"
              placeholder="Enter your password..."
            />
            {server_error.password ? (
              <span style={{ fontSize: 12, color: "red", paddingTop: 10 }}>
                {server_error.password[0]}
              </span>
            ) : (
              ""
            )}

            <label>Password Confirm</label>
            <input
              className="registerInput"
              type="password"
              name="password2"
              placeholder="Enter your Password Confirm..."
            />
            {server_error.password2 ? (
              <span style={{ fontSize: 12, color: "red", paddingTop: 10 }}>
                {server_error.password2[0]}
              </span>
            ) : (
              ""
            )}
            <button type="submit" className="registerButton">
              Register
            </button>
            {server_error.non_field_errors ? (
              <span severity="error">{server_error.non_field_errors[0]}</span>
            ) : (
              ""
            )}
          </form>
          <button className="registerLoginButton">Login</button>
        </div>
      )}
    </>
  );
}
