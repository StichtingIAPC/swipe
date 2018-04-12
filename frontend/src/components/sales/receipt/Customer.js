import React from 'react';
import { connect } from 'react-redux';

class Customer extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		return (
			<div className="row">
				This component does not as of yet exist. Sorry.

				<div className="col-xs-8 col-md-8">
					{this.props.requirementsLoaded ? this.props.children : null}
				</div>

			</div>
		);
	}
}

export default connect(
	state => ({
		...connectMixin({
		 }, state
		),
		state,
	})
)(Customer);
