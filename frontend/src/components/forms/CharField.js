import React from 'react';
import PropTypes from 'prop-types';

/**
 * Created by Matthias on 27/11/2016.
 */

export default class CharField extends React.Component {
	render() {
		const { name, className, value, minLength, maxLength, ...rest } = this.props;

		return (
			<div className={className}>
				<label className="col-sm-3 control-label" htmlFor={name}>{name}</label>
				<div className="col-sm-9">
					<input
						className="form-control"
						type="text"
						id={name}
						value={value}
						minLength={minLength}
						maxLength={maxLength}
						{...rest} />
				</div>
			</div>
		);
	}
}

CharField.propTypes = {
	name: PropTypes.string.isRequired,
	value: PropTypes.string.isRequired,
	minLength: PropTypes.number.isRequired,
	maxLength: PropTypes.number.isRequired,
	className: PropTypes.string,
};

CharField.defaultProps = { className: 'form-group' };
