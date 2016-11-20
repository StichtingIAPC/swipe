import React  from 'react';
import { Link } from 'react-router';
import autoBind from 'react-autobind';
import auth from '../../../core/auth';
import Glyphicon from '../../../../../tools/static/tools/components/Glyphicon';

export class UserBlock extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			open: false,
		};
		autoBind(this);
	}

	toggleDropdown(evt) {
		this.setState({open: !this.state.open});
		evt.preventDefault();
	}

	login() {
		auth.startAuthentication();
	}

	render() {
		if (auth.isAuthenticated()) {
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
								<small>{user.description}</small>
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
					<Link to="/" onClick={this.login.bind(this)} className="user-link login">
						<Glyphicon glyph="log-in" x-class="top-bar-icon" />
						<span>Login</span>
					</Link>
				</li>
			);
		}
	}
}

UserBlock.propTypes = {};

export default UserBlock;
