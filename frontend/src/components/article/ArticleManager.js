import React from "react";
import { connect } from "react-redux";
import { Link } from "react-router";
import { push } from "react-router-redux";
import { connectMixin, fetchStateRequirementsFor } from "../../core/stateRequirements";
import { articles } from "../../actions/articles";
import { labels } from "../../actions/assortment/labels";
import { labelTypes } from "../../actions/assortment/labelTypes";
import ArticleSelector from "./ArticleSelector";
import FontAwesome from "../tools/icons/FontAwesome";
import { accountingGroups } from "../../actions/money/accountingGroups";

class ArticleManager extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		if (!this.props.requirementsLoaded) return null;

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
		)
	}
}

export default connect(
	connectMixin({
		articles,
		labels,
		labelTypes,
		accountingGroups,
	}),
	dispatch => ({
		dispatch: dispatch,
		selectArticle: (article) => dispatch(push(`/articlemanager/${article.id}/`)),
	})
)(ArticleManager)
