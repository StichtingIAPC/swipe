import React, { PropTypes } from "react";
import { connect } from "react-redux";

function AssortmentLabel({labels, labelTypeID, labelValue}) {
	const labelType = labels.find(label => label.id === labelTypeID);

	return <span className="label label-sm label-primary">
		{labelType && labelType.name}:{labelValue}
	</span>
}

AssortmentLabel.propTypes = {
	labels: PropTypes.object.isRequired,
	labelTypeID: PropTypes.number.isRequired,
	labelValue: PropTypes.string.isRequired,
};

export default connect(state => ({
	labels: state.labels ? state.labels.labels || [] : [],
}))(AssortmentLabel)

