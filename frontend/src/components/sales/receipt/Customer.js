import React from 'react';
import PropTypes from 'prop-types';

export default class Customer extends React.Component {
	render() {
		return <div style={{ border: '1px solid black' }}>
			Customer selector
		</div>;
	}
}

Customer.propTypes = {
	onChange: PropTypes.func.isRequired,
	customer: PropTypes.object,
};
