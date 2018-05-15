import React from 'react';

import PropTypes from 'prop-types';

export default class Receipt extends React.Component {
	render() {
		return <div style={{ border: '1px solid black' }}>
			Receipt here!
		</div>;
	}
}

Receipt.propTypes = {
	onArticleRemove: PropTypes.func.isRequired,
	receipt: PropTypes.arrayOf(PropTypes.object).isRequired,
};

