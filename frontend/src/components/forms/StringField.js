import React from 'react';

/**
 * Created by Matthias on 18/11/2016.
 */

export default class StringField extends React.Component {
	render() {
		const {name, className, ...rest} = this.props;
		return (
			<div className={className || `form-group`}>
				<label className="col-sm-2 control-label" htmlFor={name}>{name}</label>
				<div className="col-sm-10">
					<input
						className="form-control"
						type="text"
						id={name}
						{...rest} />
				</div>
			</div>
		)
	}
}
