import React, { Component } from 'react';
import './../styles/LandingPage.scss';
import { Link } from "react-router-dom";

class App extends Component {
  constructor() {
    super();

    this.state = {
      firstName: '',
      lastName: '',
      email: '',
      password: '',
    };
  }
  render() {
    return (
      <div className="LandingPage">
        <h1>Easily transcribe audio files in just a few steps</h1>
        <div className="Button" onClick={(() => this.props.history.push('/'))}>
          Sign Up
          </div>
      </div>
    );
  }
}

export default App;
