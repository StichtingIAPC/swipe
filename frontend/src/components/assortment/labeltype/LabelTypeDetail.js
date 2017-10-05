import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router';
import FontAwesome from '../../tools/icons/FontAwesome';

class LabelTypeDetail extends React.Component {
	render() {
		const { labelType } = this.props;

		return (
			<div className="box">
				<div className="box-header with-border">
					<h3 className="box-title">Supplier: {labelType.name}</h3>
					<div className="box-tools">
						<div className="input-group">
							<div className="btn-group">
								<Link to="/assortment/" className="btn btn-default btn-sm" title="Close"><FontAwesome icon="close" /></Link>
								<Link to={`/assortment/labeltype/${labelType.id}/edit/`} className="btn btn-default btn-sm" title="Edit"><FontAwesome icon="edit" /></Link>
							</div>
						</div>
					</div>
				</div>
				<div className="box-body">
					<dl className="dl-horizontal">
						{[ 'name', 'description' ].map(
							key => (
								<div key={key}>
									<dt>{key}</dt>
									<dd>{String(labelType[key])}</dd>
								</div>
							)
						)}
						<div>
							<dt>Unit type</dt>
							<dd>{this.props.unitType.type_long}</dd>
						</div>
						<div>
							<dt>Labels</dt>
							<dd>{labelType.labels.map(el => <span key={el}>{el}</span>) || 'None'}</dd>
						</div>
					</dl>
				</div>
			</div>
		);
	}
}

export default connect(
	(state, props) => {
		const labelType = (state.labelTypes.labelTypes || []).find(el => el.id === Number(props.params.labelTypeID));

		return {
			labelType,
			unitType: (state.unitTypes.unitTypes || []).find(el => el.id === Number(labelType.unit_type)),
		};
	}
)(LabelTypeDetail);
