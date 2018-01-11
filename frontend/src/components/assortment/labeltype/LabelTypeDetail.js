import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import FontAwesome from '../../tools/icons/FontAwesome';
import { fetchLabelType } from '../../../state/assortment/label-types/actions';

class LabelTypeDetail extends React.Component {
	componentWillMount() {
		this.props.fetchLabelType(this.props.id);
	}

	componentWillReceiveProps(props) {
		if (props.id !== this.props.id) {
			this.props.fetchLabelType(props.id);
		}
	}

	render() {
		const { labelType } = this.props;

		return (
			<div className="box">
				<div className="box-header with-border">
					<h3 className="box-title">LabelType: {labelType.name}</h3>
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
							<dd>{labelType.type_long}</dd>
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

// TODO: replace with fetchers
export default connect(
	state => ({
		labelType: state.assortment.labelTypes.activeObject,
	}),
	{
		fetchLabelType,
	}
)(LabelTypeDetail);
