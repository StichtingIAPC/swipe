import React, { PropTypes } from 'react';
import { Link } from 'react-router';
import autoBind from 'react-autobind';
import { connect } from 'react-redux'

import auth from '../../../core/auth';
import Glyphicon from '../../tools/Glyphicon';

let UserBlock = class extends React.Component {
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
		if (this.props.isAuthenticated) {
			return (
				<li className={'dropdown user user-menu' + (this.state.open ? ' open' : '')}>
					<a className="dropdown-toggle" onClick={this.toggleDropdown.bind(this)}>
						<img className="user-image" title={this.props.user.username} src={this.props.user.gravatarUrl} />
						<span className="hidden-xs">{this.props.user.username}</span>
					</a>
					<ul className="dropdown-menu">
						<li className="user-header">
							<img className="img-circle" src={this.props.user.gravatarUrl} />
							<p>
								{this.props.user.username}
								<small>{this.props.user.description}</small>
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
					<Link to="#" onClick={this.login.bind(this)} className="user-link login">
						<Glyphicon glyph="log-in" x-class="top-bar-icon" />
						<span>Login</span>
					</Link>
				</li>
			);
		}
	}
};

UserBlock.propTypes = {
	'user': PropTypes.object,
	'isAuthenticated': PropTypes.bool.isRequired,
};

UserBlock = connect(
	(state, ownProps) => ({
		...ownProps,
		user: state.auth.user,
		isAuthenticated: (state.auth.user !== null),
	}),
	(dispatch, ownProps) => ({
		...ownProps,
	})
)(UserBlock);

export {
	UserBlock,
}


export default UserBlock;
