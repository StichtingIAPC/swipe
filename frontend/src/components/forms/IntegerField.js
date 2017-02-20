import React from "react";

/**
 * Created by Matthias on 18/11/2016.
 */

export default function IntegerField(props) {
	const {name, className, value, onChange, ...rest} = props;
	return (
		<div className={className || `form-group`}>
			<label className="col-sm-3 control-label" htmlFor={name}>{name}</label>
			<div className="col-sm-9">
				<input
					className="form-control"
					type="number"
					min={0}
					step={1}
					id={name}
					value={value}
					onChange={onChange}
					{...rest} />
			</div>
		</div>
	)
}
