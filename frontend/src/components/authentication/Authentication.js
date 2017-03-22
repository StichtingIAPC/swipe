import React from "react";
import { connect } from "react-redux";
import { startLogin } from "../../actions/auth.js";
import Glyphicon from "../tools/icons/Glyphicon";

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
		return <div className="page-authentication login-page">
			<div className="login-box">
				<div className="login-logo">
					<b>Swipe</b>
				</div>
				<div className="login-box-body">
					<form onSubmit={this.onSubmit.bind(this)}>
						<p className="login-box-msg">Sign in to start your session</p>
						<div className="form-group has-feedback">
							<input
								type="text"
								onChange={e => this.setState({username: e.target.value})}
								value={this.state.username}
								className="form-control" />
							<Glyphicon glyph="user form-control-feedback" />
						</div>
						<div className="form-group has-feedback">
							<input
								type="password"
								onChange={e => this.setState({password: e.target.value})}
								value={this.state.password}
								className="form-control" />
							<Glyphicon glyph="lock form-control-feedback" />
						</div>
						<div className="row">
							<div className="col-xs-8" />
							<div className="col-xs-4">
								<button type="submit" className="btn btn-primary btn-block btn-flat">Sign In</button>
							</div>
						</div>
					</form>
				</div>
			</div>
		</div>
	}
}

export default connect(
	state => ({ auth: state.auth }),
	dispatch => ({ login: (username, password) => dispatch(startLogin(username, password)) }),
)(Authentication);
