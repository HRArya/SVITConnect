import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { BEUrl } from "./BEUrl";

function post(url, body, callback) {
  let headers = new Headers();

  console.log(headers);
  headers.append("Content-Type", "application/json");
  headers.append("Accept", "application/json");
  headers.append("Origin", BEUrl);

  let formData = new FormData();
  for (const [key, value] of Object.entries(body)) {
    formData.append(key, value);
  }
  console.log(formData);

  fetch(url, {
    method: "POST",
    mode: "no-cors",
    credentials: "include",
    headers: headers,
    body: formData,
  })
    .then((json) => {
      callback(json);
    })
    .catch((err) => {
      console.log(err);
    });
}

const SignUp = (props) => {
  const [username, setUserName] = useState("");
  const [location, setLocation] = useState("");
  const [bio, setBio] = useState("");
  const [mailid, setMailId] = useState("");
  const [website, setWebsite] = useState("");
  const [firstname, setFirstName] = useState("");
  const [lastname, setLastName] = useState("");
  const [photo, setPhoto] = useState("");
  const [dateofbirth, setDateOfBirth] = useState("");
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const localuser = localStorage.getItem("username");

  useEffect(() => {
    if (localuser) {
      navigate("/");
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    localStorage.setItem("username", username);

    const Useradded = {
      username,
      location,
      bio,
      mailid,
      website,
      firstname,
      lastname,
      photo,
      dateofbirth,
      password,
    };

    console.log(Useradded);

    //navigate("/");
    post(BEUrl + "/new_user_2", Useradded, (json) => {
      console.log(json);
      window.location.reload(false);
      localStorage.setItem("username", username);
      navigate("/");
    });
  };

  return (
    <div className='create'>
      <h1>Sign Up</h1>
      <form onSubmit={handleSubmit}>
        <label>User Name:</label>
        <input
          type='text'
          pattern='[^\s]+'
          required
          onChange={(e) => setUserName(e.target.value)}
        />
        <label>Location:</label>
        <input
          type='text'
          required
          onChange={(e) => setLocation(e.target.value)}
        />
        <label>Bio:</label>
        <input type='text' required onChange={(e) => setBio(e.target.value)} />
        <label>Mail Id:</label>
        <input
          type='email'
          required
          onChange={(e) => setMailId(e.target.value)}
        />
        <label>Website:</label>
        <input type='text' onChange={(e) => setWebsite(e.target.value)} />
        <label>First Name:</label>
        <input
          type='text'
          required
          onChange={(e) => setFirstName(e.target.value)}
        />
        <label>Last Name:</label>
        <input type='text' onChange={(e) => setLastName(e.target.value)} />
        <label>Photo:</label>
        <input type='file' onChange={(e) => setPhoto(e.target.files[0])} />
        <label>Date Of Birth:</label>
        <input
          type='date' max={'2022-06-01'}
          required
          onChange={(e) => setDateOfBirth(e.target.value)}
        />
        <label>Password:</label>
        <input type='password' onChange={(e) => setPassword(e.target.value)} />

        <button>Sign Up</button>
      </form>
    </div>
  );
};

export default SignUp;
