import React from "react";
import { connect } from "react-redux";

function AssortmentLabel({labels, labelID}) {
	return <span className="label label-sm label-primary">
		{labels[labelID] ? labels[labelID].name : `Missing Label(${labelID})`}
	</span>
}

export default connect(state => ({
	labels: state.labels ? state.labels.labels || [] : [],
}))(AssortmentLabel)

