import React, { PropTypes } from "react";

export default function BoolField ({name, className, value, onChange, ...rest}) {
	return (
		<div className={className || `form-group`}>
			<label className="col-sm-3 control-label" htmlFor={name}>{name}</label>
			<div className="col-sm-9">
				<input
					className="checkbox"
					type="checkbox"
					id={name}
					checked={value}
					value={value}
					onChange={onChange}
					{...rest} />
			</div>
		</div>
	)
}

BoolField.propTypes = {
	name: PropTypes.string.isRequired,
	value: PropTypes.oneOfType([PropTypes.bool, PropTypes.string]).isRequired,
	className: PropTypes.string,
};

BoolField.defaultProps = {
	className: 'form-group',
};
