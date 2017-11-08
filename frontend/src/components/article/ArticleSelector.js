import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import articles from '../../state/assortment/articles/actions.js';
import { labelTypes } from '../../state/assortment/label-types/actions.js';
import { unitTypes } from '../../state/assortment/unit-types/actions.js';
import { connectMixin, fetchStateRequirementsFor } from '../../core/stateRequirements';
import FontAwesome from '../tools/icons/FontAwesome';
import LabelList from '../assortment/LabelList';

class ArticleSelector extends React.Component {
	constructor(props) {
		super(props);
		this.renderArticle = this.renderArticle.bind(this);
	}

	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	select(article) {
		this.props.onSelect(article);
	}

	renderArticle({ article }) {
		return (
			<li className="item" onClick={() => this.select(article)}>
				<div className="product-info">
					<a className="product-title">
						{article.name}
						<span className="label label-danger pull-right">{article.price}</span>
					</a>
					<LabelList labels={article.labels} className="product-description" />
				</div>
			</li>
		);
	}

	render() {
		return (
			<div className="box">
				<div className="box-header with-border">
					<h3 className="box-title">Search Articles</h3>
					<div className="box-tools">
						<div className="input-group">
							<div className="btn-group">
								<Link
									onClick={this.props.updateList}
									className="btn btn-default btn-sm"
									title="Reload">
									<FontAwesome icon="repeat" />
								</Link>
								{
									this.props.toolButtons ?
										this.props.toolButtons :
									 null
								}
							</div>
						</div>
					</div>
				</div>
				<div
					style={{
						maxHeight: 'calc(100vh - 144px)',
						overflow: 'auto',
					}}
					className="box-body">
					<ul className="products-list product-list-in-box">
						{this.props.articles.map(el => <this.renderArticle key={el.id} article={el} />)}
					</ul>
				</div>
			</div>
		);
	}
}

export default connect(
	state => ({
		...connectMixin({
			assortment: {
				articles,
				labelTypes,
				unitTypes,
			},
		}, state),
		articles: state.assortment.articles.articles,
	}),
	{
		updateList: articles,
	}
)(ArticleSelector);
