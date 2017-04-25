import React from "react";
import { connect } from "react-redux";
import { Link } from "react-router";
import AssortmentLabel from "./AssortmentLabel";

export default function LabelList ({labels, insert, ...rest}) {
	const Insert = insert;
	return <div {...rest}>
		{[].concat(Object.entries(labels).map(([ltID, values]) => (
			values.map(
				lValue => (
					<AssortmentLabel key={`${ltID}-${lValue}`} labelTypeID={Number(ltID)} labelValue={lValue}>
						{Insert ? <Insert value={lValue} typeID={ltID} /> : null}
					</AssortmentLabel>
				)
			)
		)))}
	</div>
}
