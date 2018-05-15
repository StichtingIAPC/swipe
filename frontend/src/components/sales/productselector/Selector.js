import React from 'react';
import PropTypes from 'prop-types';

export default class Selector extends React.Component {
	render() {
		return <div style={{ border: '1px solid black' }}>
			Stock selector
		</div>;
	}
}

Selector.propTypes = {
	onArticleRemove: PropTypes.func.isRequired,
	receipt: PropTypes.array.isRequired,
	stock: PropTypes.array.isRequired,
};
