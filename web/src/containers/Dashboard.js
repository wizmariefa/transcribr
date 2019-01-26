import React, { Component } from 'react';
import './../styles/Dashboard.scss';
import client from './../util/client';
import ConnectGoogleCloud from './../components/ConnectGoogleCloud';

class Login extends Component {
  constructor() {
    super();
    this.state = {};
  }
  render() {
    return (
      <div className="Page Dashboard">
        <div className="Navigation">
            <h1 className="Logo">transcribr.io</h1>
            <ConnectGoogleCloud />
        </div>
        
      </div>
    );
  }
}

export default Login;
