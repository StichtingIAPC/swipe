import React from 'react'

import { Link } from 'react-router';

import Glyphicon from 'tools/components/Glyphicon';
import FontAwesome from 'tools/components/FontAwesome';
import auth from 'www/auth';

/**
 * Created by Matthias on 05/11/2016.
 */

export class SBLink extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      open: null,
    };
  }

  toggle(evt) {
    this.setState({
      open: this.state.open ? null : 'active',
    });
    evt.preventDefault();
  }

  render() {
    const children = this.props.children ? (
      <ul className={'treeview-menu' + (this.state.open ? ' menu-open' : '')}>
        {this.props.children}
      </ul>
    ) : null;

    const openswitch = this.props.children ? (
      <span className="pull-right-container" onClick={this.toggle.bind(this)}>
        <FontAwesome icon={(this.state.open?"angle-down":"angle-left") + " pull-right"}/>
      </span>
    ) : null;

    return (
      <li className={this.state.open ? 'treeview active' : 'treeview'}>
        <Link to={this.props.to} activeClassName={this.props.activeClassName || "active"}>
          <FontAwesome icon={this.props.icon ? this.props.icon : 'circle-o'}/>
          <span>{this.props.text}</span>
          {openswitch}
        </Link>
        {children}
      </li>
    );
  }
}

export class Sidebar extends React.Component {
  render() {
    const login_logout = auth.isLoggedIn()? (
      <SBLink to="/logout" text="Log out" glyph="log-out"/>
    ) : (
      <SBLink to="/login" text="Log in" glyph="log-in"/>
    );

    return (
      <aside className="main-sidebar">
        <section className="sidebar">
          <ul className="sidebar-menu">
            {this.props.children}
            <li><br/></li>
            {login_logout}
          </ul>
        </section>
      </aside>
    )
  }
}
