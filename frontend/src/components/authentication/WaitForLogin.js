import React, { Component } from 'react';
import { connect } from 'react-redux';

export class WaitForLogin extends Component {
	render() {
		if (!this.props.user) {
			return <div />;
		}
		return this.props.children;
	}
}

export default connect(
	state => ({
		user: state.auth.currentUser,
	})
)(WaitForLogin);
