import { useState } from "react";

export default function Form(props) {
  const [name, setName] = useState("");

  function handleChange(e) {
    setName(e.target.value);
  }

  function handleSubmit(e) {
    e.preventDefault();
    props.addTask(name);
    setName("");
  }

  return (
    <form>
      <h2 className="label-wrapper">
        <label htmlFor="new-todo-input" className="label__lg">
          What needs to be done?
        </label>
      </h2>
      <input
        type="text"
        id="new-todo-input"
        className="input input__lg"
        name="text"
        value={name}
        autoComplete="off"
        onChange={handleChange}
      />
      <button
        type="submit"
        className="btn btn__primary btn__lg"
      >
        Add
      </button>
    </form>
  );
}
