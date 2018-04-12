import React from 'react';
import { connect } from 'react-redux';
import { Switch, Route, Link } from 'react-router-dom';
import { push } from 'react-router-redux';
import articles from '../../state/assortment/articles/actions.js';
import { labelTypes } from '../../state/assortment/label-types/actions.js';
import { unitTypes } from '../../state/assortment/unit-types/actions.js';
import ArticleSelector from './ArticleSelector';
import FontAwesome from '../tools/icons/FontAwesome';
import { accountingGroups } from '../../state/money/accounting-groups/actions.js';
import ArticleEdit from './ArticleEdit';

class ArticleManager extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		const { match } = this.props;

		if (!this.props.requirementsLoaded) {
			return null;
		}

		return (
			<div className="row">
				<div className="col-sm-4">
					<ArticleSelector
						onSelect={this.props.selectArticle}
						toolButtons={[
							<Link
								key="hello"
								to="/articlemanager/create/"
								className="btn btn-success btn-sm"
								title="Create"><FontAwesome icon="plus" /></Link>,
						]} />
				</div>
				<div className="col-sm-8">
					<Switch>
						<Route key="new" path={`${match.path}/new`} component={ArticleEdit} />
						<Route key="old" path={`${match.path}/:articleID`} component={ArticleEdit} />
					</Switch>
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
