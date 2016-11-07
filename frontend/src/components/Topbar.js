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
      dropdownElement: null,
    }
  }

  componentDidMount() { // add dropdown if logged in.
    if (auth.isLoggedIn()) {
      this.addDropdownActive()
    }
  }

  addDropdownActive() {
    this.setState({
      dropdownElement: new Foundation.DropdownMenu(
        jQuery(document.getElementById('user-dropdown'))
      )
    });
  }

  removeDropdownActive() {
    try {
      this.state.dropdownElement.$element.foundation('destroy');
    } catch (e) {} finally {
      this.setState({dropdownElement: null})
    }
  }

  shouldComponentUpdate() { // update if login state does not match the state of the dropdown.
    return auth.isLoggedIn() != (this.state.dropdownElement !== null);
  }

  componentWillUpdate() { // remove dropdown functionality when it does exist but no-one is logged in
    if (!auth.isLoggedIn() && this.state.dropdownElement !== null) {
      this.removeDropdownActive();
    }
  }

  componentDidUpdate() { // add dropdown functionality when it does not exist and there is a user logged in
    if (auth.isLoggedIn() && this.state.dropdownElement === null) {
      this.addDropdownActive();
    }
  }

  componentWillUnmount() { // destroy the dropdown handler if it still exists
    if (this.state.dropdownElement !== null) {
      this.removeDropdownActive();
    }
  }

  render() {
    if (auth.isLoggedIn()) {

      return (
        <ul id="user-dropdown" className="dropdown menu align-right" data-dropdown-menu>
          <li className="is-dropdown-submenu-parent" >
            <Link to={`/`} className="user-link">{auth.username} <img title={auth.username}
                                                                      src={auth.getUser().gravatar_url}/></Link>
            <ul className="menu">
              <li><Link to={`/profile`}>Profile</Link></li>
              <li><Link to="/logout">Logout</Link></li>
            </ul>
          </li>
        </ul>
      )
    }
    return (
      <ul className="menu align-right">
        <li>
          <Link to="/login" className="user-link login">
            Login
            <Glyphicon glyph="log-in" x-class="top-bar-icon"/>
          </Link>
        </li>
      </ul>
    );
  }
}
export default class Topbar extends React.Component {
  constructor({name='Page', ...rest}) {
    super({name, ...rest});
    this.name = name;
  }

  render() {
    return (
      <div className="top-bar sticky">
        <div className="top-bar-left">
          <h1>{this.name}</h1>
        </div>
        <div className="top-bar-right"><UserBlock/></div>
      </div>
    )
  }
}
