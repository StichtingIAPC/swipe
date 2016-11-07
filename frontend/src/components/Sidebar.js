import React from 'react'

import { Link } from 'react-router';

import Glyphicon from 'tools/components/Glyphicon';
import auth from 'www/auth';

/**
 * Created by Matthias on 05/11/2016.
 */

export default class Sidebar extends React.Component {
  render() {
    const login_logout = auth.isLoggedIn()? (
      <Link to="/logout">
        Log out
        <Glyphicon glyph="log-out" x-class="side-bar-icon"/>
      </Link>
    ) : (
      <Link to="/login">
        Log in
        <Glyphicon glyph="log-in" x-class="side-bar-icon"/>
      </Link>
    );

    return (
      <div className="side-bar">
        <ul className="side-bar-nav">
          <li>
            <Link to={`/dashboard`}>
              Swipe
              <Glyphicon glyph="home" x-class="side-bar-icon"/>
            </Link>
          </li>
          <li><br/></li>
          {React.Children.map(this.props.children, (child) => <li>{child}</li>)}
          <li><br/></li>
          <li>{login_logout}</li>
        </ul>
      </div>
    )
  }
}
