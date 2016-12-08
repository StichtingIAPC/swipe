import React from 'react';
import { connect } from 'react-redux';
import { push } from 'react-router-redux';

class Dashboard extends React.Component {
	toHw(event) {
		event.preventDefault();
		this.props.toHw();
		return false;
	}

	render() {
		return <div><span>Dashboard </span><a onClick={this.toHw.bind(this)}>Naar HW</a></div>
	}
}

export default connect(
	null,
	dispatch => ({ toHw: () => dispatch(push('/helloworld')) })
)(Dashboard);

/*
export default function Dashboard() {
	return (
		<div className="row">
			<div className="col-xs-6">
				<div className="box box-success">
					<div className="box-header">
						<h3 className="box-title">Welcome!</h3>
					</div>
					<div className="box-body">
						<span>Welcome to the magical swipe dashboard. It is currently very clean.</span>
					</div>
				</div>
			</div>
		</div>
	);
}
*/
