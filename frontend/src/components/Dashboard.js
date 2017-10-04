import React from "react";
import { connect } from "react-redux";
import { push } from "react-router-redux";

class Dashboard extends React.Component {
	toHw(event) {
		event.preventDefault();
		this.props.toHw();
		return false;
	}

	render() {
		return <div><span>Dashboard </span><a onClick={::this.toHw}>Naar HW</a></div>;
	}
}

export default connect(
	null,
	{
		toHw: () => push('/helloworld'),
	}
)(Dashboard);
