
import { setUserToken } from '../features/authSlice';
import axios from 'axios'

const EXPIRE_TIME_ACCESS = 1000 * 60 * 60 * 24 * 60;
const EXPIRE_TIME_REFRESH = 1000 * 60 * 60 * 24 * 10;
const storeToken = (value) => {
  if (value) {
    console.log(value)
    const { access, refresh } = value
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
  }
}

const getToken = () => {
  let access_token = localStorage.getItem('access_token')
  let refresh_token = localStorage.getItem('refresh_token')
  return { access_token, refresh_token }
}

const removeToken = () => {

  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}
// const expiredToken = () => {
//   setTimeout(function () {
//     console.log(1)
//     removeToken();
//   }, EXPIRE_TIME);
// }
function ExpiredToken(dispatch) {
  setTimeout(function () {
    localStorage.removeItem('access_token')
    if (getToken().refresh_token) {
      console.log(getToken().refresh_token)
      axios.
        post('http://localhost:8000/api/token/refresh/', { refresh: getToken().refresh_token }).
        then((res) => {
          console.log(res.data)
          storeToken({ access: res.data.access, refresh: getToken().refresh_token })
          dispatch(
            setUserToken({
              access_token: res.data,
            })
          );
          ExpiredToken(dispatch)
        }).
        catch((err) => { })
    }
  }, EXPIRE_TIME_ACCESS);
}

function ExpiredRefreshToken(dispatch) {
  setTimeout(function () {
    localStorage.removeItem('refresh_token')
    dispatch(
      setUserToken({
        access_token: '',
      })
    );
  }, EXPIRE_TIME_REFRESH);
}

export { storeToken, getToken, removeToken, ExpiredToken, ExpiredRefreshToken }