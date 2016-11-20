import React from 'react';

/**
 * Created by Matthias on 18/11/2016.
 */

export default class DecimalField extends React.Component {
	render() {
		return (
			<input
				className="form-control"
				type="number"
				min="0"
				step="0.00001"
				value={this.props.value}
				onChange={this.props.onChange} />
		)
	}
}
