import React, {PropTypes} from "react";

/**
 * Created by Matthias on 18/11/2016.
 */

export default class StringField extends React.Component {
	render() {
		const {name, className, value, ...rest} = this.props;
		return (
			<div className={className}>
				<label className="col-sm-3 control-label" htmlFor={name}>{name}</label>
				<div className="col-sm-9">
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
	value: PropTypes.string.isRequired,
	className: PropTypes.string,
};

StringField.defaultProps = {
	className: 'form-group',
};
