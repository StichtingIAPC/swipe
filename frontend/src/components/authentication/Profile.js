import React from 'react';
import { connect } from 'react-redux';
import { push } from 'react-router-redux';

class Profile extends React.Component {

	render() {
		return (
		    <div className="row">
                <div className="col-sm-4">
		            {this.props.user.username}
                </div>
                <div className="col-sm-8">
                    {this.props.user.email}
                </div>
                <div className="col-sm-8">
                    {this.props.user.firstName}
                </div>
                <div className="col-sm-8">
                    {this.props.user.lastName}
                </div>
                <div className="col-sm-8">
                    {this.props.user.gravatarUrl}
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
