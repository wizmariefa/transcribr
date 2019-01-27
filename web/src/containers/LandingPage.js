import React, { Component } from 'react';
import './../styles/LandingPage.scss';
import { Link } from "react-router-dom";

class LandingPage extends Component {
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
      <div className="LandingPage FlexColumn JustifyCenter AlignCenter">
        <h1>Easily transcribe audio files in just a few steps</h1>
        <div className="Button" onClick={(() => this.props.history.push('/register'))}>
          Sign Up
          </div>
          <div className="Button" onClick={(() => this.props.history.push('/login'))}>
          Login
          </div>
      </div>
    );
  }
}

export default LandingPage;
