import { useState } from "react";
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

const NewPoll = () => {
  const [Question, setQuestion] = useState("");
  const [optiona, setoptiona] = useState("");
  const [optionb, setoptionb] = useState("");
  const [optionc, setoptionc] = useState("");
  const username = localStorage.getItem("username");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    const poll_body = { Question, optiona, optionb, optionc, username };

    post(BEUrl + "/new_poll", poll_body, (res) => {
      console.log(res);
      navigate("/polls");
    });
  };

  return (
    <div className='create'>
      <h2>New Poll</h2>
      <form onSubmit={handleSubmit}>
        <label>Question :</label>
        <input
          type='text'
          required
          onChange={(e) => setQuestion(e.target.value)}
        />
        <label>Option A :</label>
        <input
          type='text'
          required
          onChange={(e) => setoptiona(e.target.value)}
        />
        <label>Option B :</label>
        <input
          type='text'
          required
          onChange={(e) => setoptionb(e.target.value)}
        />
        <label>Option C :</label>
        <input type='text' onChange={(e) => setoptionc(e.target.value)} />
        <button>Add Poll</button>
      </form>
    </div>
  );
};

export default NewPoll;
