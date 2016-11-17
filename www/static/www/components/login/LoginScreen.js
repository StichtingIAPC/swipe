import React from 'react';

import { LoginBase, LoginForm, LogoutForm } from 'www/components/login/LoginBase';

import auth from 'www/auth'

/**
 * Created by Matthias on 06/11/2016.
 */

export class LoginScreen extends React.Component {
  login({username, password}) {

  }

  render() {
    return (
      <LoginBase>
        <h1>Login</h1>
        <LoginForm after_login="/dashboard"/>
      </LoginBase>
    );
  }
}

export class LogoutScreen extends React.Component {
  render() {
    return (
      <LoginBase>
        <h1>Logout</h1>
        <LogoutForm after_logout="/"/>
      </LoginBase>
    )
  }
}
