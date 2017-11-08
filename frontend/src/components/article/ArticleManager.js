import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { push } from 'react-router-redux';
import { connectMixin, fetchStateRequirementsFor } from '../../core/stateRequirements';
import articles from '../../state/assortment/articles/actions.js';
import { labelTypes } from '../../state/assortment/label-types/actions.js';
import { unitTypes } from '../../state/assortment/unit-types/actions.js';
import ArticleSelector from './ArticleSelector';
import FontAwesome from '../tools/icons/FontAwesome';
import { accountingGroups } from '../../state/money/accounting-groups/actions.js';

class ArticleManager extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		if (!this.props.requirementsLoaded) {
			return null;
		}

		return (
			<div className="row">
				<div className="col-sm-4">
					<ArticleSelector
						onSelect={this.props.selectArticle}
						toolButtons={
							<Link
								to="/articlemanager/create/"
								className="btn btn-success btn-sm"
								title="Create"><FontAwesome icon="plus" /></Link>
						} />
				</div>
				<div className="col-sm-8">
					{this.props.children}
				</div>
			</div>
		);
	}
}

export default connect(
	connectMixin({
		assortment: {
			articles,
			labelTypes,
			unitTypes,
		},
		money: {
			accountingGroups,
		},
	}),
	{
		dispatch: evt => evt,
		selectArticle: article => push(`/articlemanager/${article.id}/`),
	}
)(ArticleManager);
