import React from 'react';
import { Link } from 'react-router';

import '../jQueryFix'

import 'foundation-sites/js/foundation.core'
import 'foundation-sites/js/foundation.util.keyboard'
import 'foundation-sites/js/foundation.util.box'
import 'foundation-sites/js/foundation.util.nest'
import 'foundation-sites/js/foundation.dropdownMenu'

import auth from 'www/auth';

import Glyphicon from 'tools/components/Glyphicon'

/**
 * Created by Matthias on 05/11/2016.
 */

class UserBlock extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      open: false,
    }
  }

  toggleDropdown(evt) {
    this.setState({open: !this.state.open});
    evt.preventDefault();
  }

  render() {
    if (auth.isLoggedIn()) {
      const user = auth.getUser();

      return (
        <li className={"dropdown user user-menu" + (this.state.open? ' open' : '')}>
          <a className="dropdown-toggle" onClick={this.toggleDropdown.bind(this)}>
            <img className="user-image" title={user.username} src={user.gravatar_url}/>
            <span className="hidden-xs">{user.username}</span>
          </a>
          <ul className="dropdown-menu">
            <li className="user-header">
              <img class="img-circle" src={user.gravatar_url} />
              <p>
                {user.username}
                <small>{user.desciprion}</small>
              </p>
            </li>
            <li className="user-footer">
              <div className="pull-left">
                <Link to="/profile" className="btn btn-default btn-flat">Profile</Link>
              </div>
              <div className="pull-right">
                <Link to="/logout" className="btn btn-default btn-flat">Logout</Link>
              </div>
            </li>
          </ul>
        </li>
      )
    } else {
      return (
        <li className="dropdown user user-menu">
          <Link to="/login" className="user-link login">
            <Glyphicon glyph="log-in" x-class="top-bar-icon"/>
            Login
            </Link>
        </li>
      );
    }
  }
}
export default class Topbar extends React.Component {
  render() {
    return (
      <header className="main-header">
        <a className="logo">
          <span className="logo-mini">Sw</span>
          <span className="logo-lg">Swipe</span>
        </a>
        <nav className="navbar navbar-static-top" role="navigation">
          <a className="sidebar-toggle" onClick={this.props.sidebar_toggle}/>
          <div className="navbar-custom-menu pull-left">
            <ul className="nav navbar-nav">
              <li>
                <a>{this.props.name || "page"}</a>
              </li>
            </ul>
          </div>
          <div className="navbar-custom-menu">
            <ul className="nav navbar-nav">
              <UserBlock user={auth.getUser()}/>
            </ul>
          </div>
        </nav>
      </header>
    )
  }
}
