import React, { Component } from 'react';
import './../styles/Dashboard.scss';
import client from './../util/client';
import ConnectGoogleCloud from './../components/ConnectGoogleCloud';
import TranscribrDropzone from './../components/TranscribrDropzone';
import url from 'url';

class Dashboard extends Component {
  constructor() {
    super();
    this.state = {};
  }
  componentDidMount() {
    this.connectGoogleOAuth();
  }
  connectGoogleOAuth() {
    let location = window.location
    let hash = location.hash.split('').slice(1).join('');
    let params = hash
        .split("&")
        .map(v => v.split("="))
        .reduce((pre, [key, value]) => ({ ...pre, [key]: value }), {});

    if(params.access_token) {
        let {
            access_token,
            expires_in,
            scope,
            token_type,
        } = params;

        client.connectOAuth({ access_token, expires_in, scope, token_type })
            .then(res => {
                // window.location.hash = '';
                console.log(res);
            })
            .catch(err => console.error(err));
    }

    
  }
  getUser() {

  }
  render() {
    return (
      <div className="Page Dashboard">
        <div className="Navigation">
            <h1 className="Logo">transcribr.io</h1>
            <ConnectGoogleCloud />
        </div>
        <TranscribrDropzone />
      </div>
    );
  }
}

export default Dashboard;
