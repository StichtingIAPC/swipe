import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

class AssortmentLabel extends React.Component {
	render() {
		const {
			labelTypes,
			unitTypes,
			labelTypeID,
			labelValue,
			children,
		} = this.props;

		const labelType = labelTypes.find(label => label.id === labelTypeID) || {};
		const unitType = unitTypes.find(el => el.id === +labelType.unit_type) || {};

		return <span className="article-label default">
			<span>{labelType.name}</span>
			<span>{labelValue}{unitType.type_short}</span>
			{children}
		</span>;
	}
}

AssortmentLabel.propTypes = {
	labelTypeID: PropTypes.number.isRequired,
	labelValue: PropTypes.string.isRequired,
};

export default connect(
	state => ({
		labelTypes: state.assortment.labelTypes.labelTypes,
		unitTypes: state.assortment.unitTypes.unitTypes,
	}),
	null
)(AssortmentLabel);
