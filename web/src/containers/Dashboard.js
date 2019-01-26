import React, { Component } from 'react';
import './../styles/Dashboard.scss';
import { Link } from 'react-router-dom';
import client from './../util/client';
import getOAuthUrl from './../util/getOAuthUrl';

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
            <a href={getOAuthUrl('http://localhost:3000')}>
                <div className="Button">Connect Google Account</div>
            </a>
        </div>
        
      </div>
    );
  }
}

export default Login;
