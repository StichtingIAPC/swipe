import React from 'react';
import PropTypes from 'prop-types';

import { Link } from 'react-router-dom';
import { push } from 'react-router-redux';

import { connect } from 'react-redux';
import { logout } from '../../../state/auth/actions.js';

class UserBlock extends React.Component {
	constructor(props) {
		super(props);
		this.state = { open: false };
	}

	toggleDropdown = evt => {
		this.setState({ open: !this.state.open });
		evt.preventDefault();
	};

	componentWillReceiveProps(newProps) {
		if (!newProps.isAuthenticated && this.state.open) {
			this.setState({ open: false });
		}
	}

	gotoProfile = evt => {
		this.toggleDropdown(evt);
		this.props.selectProfile();
	}

	render() {
		if (this.props.user !== null) {
			return (
				<li className={`dropdown user user-menu${this.state.open ? ' open' : ''}`}>
					<a className="dropdown-toggle" onClick={this.toggleDropdown}>
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
								<a onClick={this.gotoProfile} className="btn btn-default btn-flat">Profile</a>
							</div>
							<div className="pull-right">
								<a onClick={this.props.logout} className="btn btn-default btn-flat">Logout</a>
							</div>
						</li>
					</ul>
				</li>
			);
		}
		return (
			<li className={`dropdown user user-menu${this.state.open ? ' open' : ''}`}>
				<a className="dropdown-toggle" onClick={this.toggleDropdown}>
					<span className="hidden-xs">User not found!</span>
				</a>
				<ul className="dropdown-menu">
					<li className="user-header">
						<p>
							User not found!
						</p>
					</li>
					<li className="user-footer">
						<div className="pull-right">
							<a onClick={this.props.logout} className="btn btn-default btn-flat">Logout</a>
						</div>
					</li>
				</ul>
			</li>
		);
	}
}

UserBlock.propTypes = {
	user: PropTypes.object,
	isAuthenticated: PropTypes.bool.isRequired,
};

export default connect(
	state => ({
		user: state.auth.currentUser,
		isAuthenticated: state.auth.currentUser !== null,
	}),
	dispatch => ({
		logout: () => dispatch(logout()),
		selectProfile: () => dispatch(push('/profile')),
	}),
)(UserBlock);
