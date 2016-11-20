import React from 'react';

/**
 * Created by Matthias on 18/11/2016.
 */

export default class IntegerField extends React.Component {
	render() {
		return (
			<input
				className="form-control"
				type="number"
				min="0"
				step="1"
				value={this.props.value}
				onChange={this.props.onChange} />
		)
	}
}
