import React from 'react';

/**
 * Created by Matthias on 18/11/2016.
 */

export default class IntegerField extends React.Component {
	render() {
		const {name, className, ...rest} = this.props;
		return (
			<div className={className || `form-group`}>
				<label className="col-sm-2 control-label" htmlFor={name}>{name}</label>
				<div className="col-sm-10">
					<input
						className="form-control"
						type="number"
						min="0"
						step="1"
						value={this.props.value}
						onChange={this.props.onChange} />
				</div>
			</div>
		)
	}
}
