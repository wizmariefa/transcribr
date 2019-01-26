import React, { Component } from 'react';
import { Switch, Route } from 'react-router-dom';
import LandingPage from "./containers/LandingPage";
import Register from "./containers/Register";
import Login from './containers/Login';
import Studies from "./components/Studies";
import Study from './components/Study';
import CreateStudy from './components/CreateStudy';


class App extends Component {
  render() {
    return (
      <main className="App">
        <Switch>
          <Route exact path="/" component={LandingPage} />
          <Route exact path="/register" component={Register} />
          <Route exact path="/login" component={Login} />
        </Switch>
      </main>
    );
  }
}

export default App;
