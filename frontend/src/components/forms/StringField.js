import React, { PropTypes } from 'react';

export default class StringField extends React.Component {
	render() {
		const {name, className, value, ...rest} = this.props;
		return (
			<div className={className || `form-group`}>
				<label className="col-sm-2 control-label" htmlFor={name}>{name}</label>
				<div className="col-sm-10">
					<input
						className="form-control"
						type="text"
						id={name}
						value={value}
						{...rest} />
				</div>
			</div>
		)
	}
}

StringField.propTypes = {
	name: PropTypes.string.isRequired,
	value: PropTypes.any.isRequired,
	className: PropTypes.string,
};

StringField.defaultProps = {
	name: '',
	value: '',
};
