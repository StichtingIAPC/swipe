import React from "react";
import PropTypes from "prop-types";
import { Link } from "react-router";
import { connect } from "react-redux";
import { loginReset } from "../../../actions/auth";

class UserBlock extends React.Component {
	constructor(props) {
		super(props);
		this.state = { open: false };
	}

	toggleDropdown(evt) {
		this.setState({ open: !this.state.open });
		evt.preventDefault();
	}

	componentWillReceiveProps(newProps) {
		if (!newProps.isAuthenticated && this.state.open)
			this.setState({ open: false });
	}

	render() {
		return (
			<li className={`dropdown user user-menu${this.state.open ? ' open' : ''}`}>
				<a className="dropdown-toggle" onClick={::this.toggleDropdown}>
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
							<Link onClick={this.props.logout} className="btn btn-default btn-flat">Logout</Link>
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
	dispatch => ({ logout: () => dispatch(loginReset()) })
)(UserBlock);
