import React from 'react';
import { connect } from 'react-redux';
import { push } from 'react-router-redux';

class HelloWorld extends React.Component {
	toDash(event) {
		event.preventDefault();
		this.props.toDashboard();
		return false;
	}

	render() {
		return <div><span>Hello World <a onClick={::this.toDash}>To dashboard</a></span></div>;
	}
}

export default connect(
	null,
	dispatch => ({ toDashboard: () => dispatch(push('/dashboard')) })
)(HelloWorld);
