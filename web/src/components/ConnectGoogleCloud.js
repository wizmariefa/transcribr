import React, { Component } from 'react';
import getOAuthUrl from "./../util/getOAuthUrl";

export default class ConnectGoogleCloud extends Component {
  render() {
    return (
      <a href={getOAuthUrl('http://localhost:3000/dashboard')}>
        <div className="Button">Connect Google Account</div>
      </a>
    );
  }
}
