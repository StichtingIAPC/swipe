import React from 'react';
import PropTypes from 'prop-types';

export default function SelectField(props) {
	const { name, className, options, value, selector, nameField, ...rest } = props;

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
						opt => (
							<option key={opt[selector]} value={opt[selector] || ''}>{opt[nameField || 'name']}</option>
						)
					)}
				</select>
			</div>
		</div>
	);
}

SelectField.propTypes = {
	name: PropTypes.string.isRequired,
	className: PropTypes.string,
	value: PropTypes.oneOfType([
		PropTypes.number,
		PropTypes.string,
	]).isRequired,
	onChange: PropTypes.func.isRequired,
	selector: PropTypes.string.isRequired,
	options: PropTypes.arrayOf(PropTypes.object).isRequired,
};

SelectField.defaultProps = { selector: 'id' };
