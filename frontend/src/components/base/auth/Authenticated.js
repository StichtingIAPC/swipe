import React, { PropTypes } from 'react';
import { browserHistory } from 'react-router';
import { connect } from 'react-redux';

import Glyph from '../../tools/Glyphicon';

/**
 * Created by Matthias on 26/11/2016.
 */

let Authenticated = class extends React.Component {
	render() {
		const {component, forPermission, user, isAuthenticated, children, ...props} = this.props;
		const Component = component;
		if (isAuthenticated && user.permissions.find((el) => (el.match(forPermission) !== null)) !== undefined) {
			return (
				<Component {...props}>{children}</Component>
			)
		} else if (this.props.warn) {
			return (
				<div className="modal modal-danger" style={{display: 'block'}}>
					<div className="modal-dialog modal-md">
						<div className="modal-header">
							<button className="close" onClick={browserHistory.pop}>
								<Glyph glyph="remove" />
							</button>
							<h4 className="modal-title">You are not authorized for this part of the application</h4>
						</div>
					</div>
				</div>
			)
		} else {
			return null;
		}
	}
};

Authenticated.propTypes = {
	Component: PropTypes.func, // best way to describe a component
	forPermission: PropTypes.string,
	warn: PropTypes.bool,
};

Authenticated = connect(
	(state, ownProps) => ({
		...ownProps,
		user: state.auth.user,
		isAuthenticated: state.auth.user !== null,
	})
)(Authenticated);

export default Authenticated;
