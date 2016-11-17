import React from 'react'
import { browserHistory } from 'react-router';

import auth from 'www/auth'

/**
 * Created by Matthias on 06/11/2016.
 */

export class LoginBase extends React.Component {
  render() {
    return (
      <div className="row">
        <div className="small-10 small-offset-1 medium-8 medium-offset-2 large-6 large-offset-3">
          <div className="card">
            {this.props.children}
          </div>
        </div>
      </div>
    )
  }
}

export class LoginForm extends React.Component {
  constructor({after_login='/', ...rest}) {
    super({after_login, ...rest});
    this.state = {
      username: '',
      password: '',
      error: false,
      errorMsg: '',
    }
  }

  passChange(evt) {
    this.setState({password: evt.target.value});
  }

  userChange(evt) {
    this.setState({username: evt.target.value});
  }

  login(evt) {
    evt.preventDefault();
    auth
      .login({
          username: this.state.username,
          password: this.state.password,
        })
      .then(
      (accept) => browserHistory.push(this.props.after_login),
      (reject) => this.setState({
          error: true,
          errorMsg: reject
        })
    )
  }

  render() {
    const error_message = this.state.error? (
      <div className="callout warning">{this.state.errorMsg}</div>
    ) : '';
    return (
      <div>
        {error_message}
        <label htmlFor="username">
          Username:
          <input type="text" id="username" placeholder="jklaassen" value={this.state.username} onChange={this.userChange.bind(this)}/>
        </label>
        <label htmlFor="password">
          Password:
          <input type="password" id="password" placeholder="password" value={this.state.password} onChange={this.passChange.bind(this)}/>
        </label>
        <input type="submit" className="button small" onClick={this.login.bind(this)} value="Log in"/>
      </div>
    )
  }
}

export class LogoutForm extends React.Component {
  constructor({after_logout='/', ...rest}) {
    super({after_logout,...rest});
    this.state = {
      error: false,
      errorMsg: ''
    }
  }

  logout(evt) {
    evt.preventDefault();
    auth.logout().then(
      (accept) => browserHistory.push(this.props.after_logout),
      (reject) => this.setState({
        error: true,
        errorMsg: reject
      })
    )
  }

  render() {
    const err = this.state.error? (
      <div className="callout warning">{this.state.errorMsg}</div>
    ) : '';
    return (
      <div>
        {err}
        <button className="button danger" onClick={this.logout.bind(this)}>Log out</button>
      </div>
    )
  }
}
