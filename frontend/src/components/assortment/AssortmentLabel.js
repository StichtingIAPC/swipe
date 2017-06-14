import React from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";

let cache = {};
let lastUnitTypes = null;

function AssortmentLabel({ labelTypes, unitTypes, labelTypeID, labelValue, children, ...rest }) {
	const labelType = labelTypes.find(label => label.id === labelTypeID);

	if (unitTypes !== lastUnitTypes) {
		lastUnitTypes = unitTypes;
		cache = {};
	}
	const unitType = cache[labelType.unit_type] || (cache[labelType.unit_type] = unitTypes.find(el => el.id === +labelType.unit_type));

	return <span className="article-label default" {...rest}>
		<span>{labelType.name}</span>
		<span>{labelValue}{unitType.type_short}</span>
		{children}
	</span>;
}

AssortmentLabel.propTypes = {
	labelTypeID: PropTypes.number.isRequired,
	labelValue: PropTypes.string.isRequired,
};

export default connect(state => ({
	labelTypes: state.labelTypes.labelTypes,
	unitTypes: state.unitTypes.unitTypes,
}))(AssortmentLabel);
