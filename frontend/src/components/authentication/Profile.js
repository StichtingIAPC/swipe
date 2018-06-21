import React from 'react';
import { connect } from 'react-redux';

class Profile extends React.Component {
	render() {
		if (this.props.user === null) {
			return <div />;
		}
		return (
			<div className="box">
				<div className="box-header with-border">
					<h3 className="box-title">Profile</h3>
				</div>
				<div
					style={{
						maxHeight: 'calc(100vh - 144px)',
						overflow: 'auto',
					}}
					className="box-body">
					<p>
						<img className="user-image" title="Gravatar" src={this.props.user.gravatarUrl} />
					</p>
					<p>
						<span>Username: </span>{this.props.user.username}<br />
						<span>Email address: </span>{this.props.user.email}<br />
						<span>Name: {this.props.user.firstName} {this.props.user.lastName} </span><br />
					</p>
				</div>
			</div>
		);
	}
}

export default connect(
	state => ({
		user: state.auth.currentUser,
		isAuthenticated: state.auth.currentUser !== null,
	}),
	null
)(Profile);
