import React from 'react';
import { Link } from 'react-router';
import auth from 'www/auth';
import Glyphicon from 'tools/components/Glyphicon';

export default class UserBlock extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			open: false,
		};
	}

	toggleDropdown(evt) {
		this.setState({open: !this.state.open});
		evt.preventDefault();
	}

	render() {
		if (auth.isLoggedIn()) {
			const user = auth.getUser();

			return (
				<li className={'dropdown user user-menu' + (this.state.open ? ' open' : '')}>
					<a className="dropdown-toggle" onClick={this.toggleDropdown.bind(this)}>
						<img className="user-image" title={user.username} src={user.gravatar_url} />
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
			);
		} else {
			return (
				<li className="dropdown user user-menu">
					<Link to="/login" className="user-link login">
						<Glyphicon glyph="log-in" x-class="top-bar-icon" />
						<span>Login</span>
					</Link>
				</li>
			);
		}
	}
}
