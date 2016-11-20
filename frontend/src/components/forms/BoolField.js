import React from 'react';

/**
 * Created by Matthias on 18/11/2016.
 */

export default class BoolField extends React.Component {
	render() {
		return (
			<input
				className="checkbox"
				type="checkbox"
				value={this.props.value}
				onChange={this.props.onChange} />
		)
	}
}
