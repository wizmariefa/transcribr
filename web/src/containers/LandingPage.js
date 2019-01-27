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
      <div className="LandingPage">
        <div className="TopBanner">
          <h1 className="Logo">transcribr.io</h1>
        </div>
        <section className="container">
          <div className="LeftColumn FlexColumn">
          <div className="LeftText">Easily transcribe audio files into text with just a few steps.</div>
          <div className="LeftTextSmall">Transcribr is a simple web application designed to let people more easily
                                         convert audio files into text files for further use and analysis.</div>
          </div>
          <div className="RightColumn FlexColumn AlignCenter">
            <div className = "Whitebox FlexColumn">
            <div className = "ButtonSelect AlignLeft"> Get Started Now!
             </div>
            <div className="Button" onClick={(() => this.props.history.push('/register'))}> Sign Up </div>
            <div className="Button" onClick={(() => this.props.history.push('/login'))}> Login </div>
            </div>
          </div>
        </section>
      </div>
    );
  }
}

export default LandingPage;
