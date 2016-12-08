import React from 'react';
import { connect } from 'react-redux';
import { browserHistory } from 'react-router';

import { startLogin } from 'actions/auth.js';

class Authentication extends React.Component {
	constructor() {
		super();
		this.state = {
			username: '',
			password: '',
		};
	}

	onSubmit(event) {
		event.preventDefault();
		this.props.login(this.state.username, this.state.password);
		return false;
	}

	render() {
		return <div className="wrapper page-authentication">
			<form onSubmit={this.onSubmit.bind(this)} className="auth-form">
				<h2>Login</h2>
				<label>Username</label>
				<input type="text" onChange={e => this.setState({ username: e.target.value })} value={this.state.username} />
				<label>Password</label>
				<input type="password" onChange={e => this.setState({ password: e.target.value })} value={this.state.password} />
				<br /><button type="submit" className="btn">Login</button>
			</form>
		</div>;
	}
}

export default connect(
	state => ({ auth: state.auth }),
	dispatch => ({ login: (username, password) => dispatch(startLogin(username, password)) }),
)(Authentication);
