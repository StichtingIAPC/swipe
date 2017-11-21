import React from 'react';
import { connect } from 'react-redux';
import { push } from 'react-router-redux';

class Profile extends React.Component {

	render() {
		return (
		    <div className="row">
                <div className="col-sm-1">
                    <img className="user-image" title="Gravatar" src={this.props.user.gravatarUrl} />
                </div>
                <div className="col-sm-8">
                    <span>Username: </span>{this.props.user.username}
                </div>
                <div className="col-sm-8">
                    <span>Email address: </span>{this.props.user.email}
                </div>
                <div className="col-sm-8">
                    <span>Name: {this.props.user.firstName} {this.props.user.lastName} </span>
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
