import React from 'react';

/**
 * Created by Matthias on 18/11/2016.
 */

export default class BoolField extends React.Component {
	render() {
		const {name, className, ...rest} = this.props;
		return (
			<div className={className || `form-group`}>
				<label className="col-sm-2 control-label" htmlFor={name}>{name}</label>
				<div className="col-sm-10">
					<input
						className="checkbox"
						type="checkbox"
						value={this.props.value}
						onChange={this.props.onChange}
						{...rest} />
				</div>
			</div>
		)
	}
}
