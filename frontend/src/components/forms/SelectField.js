import React, { PropTypes } from "react";

export default function SelectField(props) {
	const { name, className, options, value, ...rest} = props;
	return (
		<div className={className || `form-group`}>
			<label className="col-sm-3 control-label" htmlFor={name}>
				{name}
			</label>
			<div className="col-sm-9">
				<select
					className="form-control"
					id={name}
					value={value}
					{...rest}>

					{(options || []).map(
						(opt) => (
							<option key={opt.id} value={opt.id}>{opt.name}</option>
						)
					)}
				</select>
			</div>
		</div>
	);
}

SelectField.proptypes = {
	name: PropTypes.string.isRequired,
	className: PropTypes.string,
	value: PropTypes.number.isRequired,

}
