import React from "react";

/**
 * Created by Matthias on 18/11/2016.
 */

export default class DecimalField extends React.Component {
	render() {
		const {name, className, ...rest} = this.props;
		return (
			<div className={className || `form-group`}>
				<label className="col-sm-3 control-label" htmlFor={name}>{name}</label>
				<div className="col-sm-9">
					<input
						className="form-control"
						type="number"
						min="0"
						step="0.00001"
						value={this.props.value}
						onChange={this.props.onChange}
						{...rest} />
				</div>
			</div>
		)
	}
}
