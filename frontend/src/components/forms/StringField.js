import React from 'react';
import PropTypes from 'prop-types';

export default function StringField({ name, className, value, onChange, ...rest }) {
	return (
		<div className={className}>
			<label className="col-sm-3 control-label" htmlFor={name}>{name}</label>
			<div className="col-sm-9">
				<input
					className="form-control"
					type="text"
					id={name}
					value={value}
					onChange={onChange}
					{...rest} />
			</div>
		</div>
	);
}

StringField.propTypes = {
	name: PropTypes.string.isRequired,
	value: PropTypes.string,
	className: PropTypes.string,
};

StringField.defaultProps = { className: 'form-group' };
