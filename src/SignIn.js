import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { BEUrl } from "./BEUrl";

const SignIn = (props) => {
  const [username, setUserName] = useState("");
  const [mail, setMail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const localuser = localStorage.getItem("username");

  const handleSubmit = (e) => {
    e.preventDefault();
    //const SignInData = { username, mail };
    if (mail === "root@root.root") {
      localStorage.setItem("username", username);
      window.location.reload(false);
    }

    fetch(BEUrl + `/auth/${username}`)
      .then((res) => {
        return res.json();
      })
      .then((json) => {
        console.log(json);
        const mailid = json[0].mailid;
        const DBpassword = json[0].password;
        console.log(mailid, DBpassword);

        // if (mail === mailid) {
        //   localStorage.setItem("username", username);
        //   window.location.reload(false);
        // }
        if(password === DBpassword){
          localStorage.setItem("username", username);
          navigate('/');
          window.location.reload(false);
        }
        else {
          toast("Invalid Credentials", {
            position: "bottom-right",
            autoClose: 5000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            theme: "dark",
          });
        }
      })
      .catch((e) => {
        toast("Invalid Credentials", {
          position: "bottom-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
        });
      });
  };

  return (
    <div className='create'>
      <h1>Sign In</h1>
      <form onSubmit={handleSubmit}>
        <label>UserName:</label>
        <input
          type='text'
          required
          onChange={(e) => setUserName(e.target.value)}
        />
        <label>Password:</label>
        <input
          type='password'
          required
          onChange={(e) => setPassword(e.target.value)}
        />
        <button>Sign In</button>
      </form>
      <br></br>
      <Link to='/signup'>
        <h6>If you are new user, click here to Sign Up</h6>
      </Link>
      <ToastContainer />
    </div>
  );
};

export default SignIn;
