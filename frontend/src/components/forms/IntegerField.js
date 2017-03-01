import React, { PropTypes } from "react";

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
					value={value}
					onChange={onChange}
					id={name}
					{...rest} />
			</div>
		</div>
	)
}

IntegerField.propTypes = {
	name: PropTypes.string.isRequired,
	value: PropTypes.oneOfType([
		PropTypes.string,
		PropTypes.number,
	]).isRequired,
	onChange: PropTypes.func.isRequired,
};
