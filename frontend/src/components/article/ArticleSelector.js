import React from "react";
import { connect } from "react-redux";
import { articles } from "../../actions/articles";
import { labels } from "../../actions/assortment/labels";
import { labelTypes } from "../../actions/assortment/labelTypes";
import { connectMixin, fetchStateRequirementsFor } from "../../core/StateRequirements";
import Label from "../assortment/AssortmentLabel";

class ArticleSelector extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	renderArticle({ article }) {
		return (<li className="item">
			<div className="product-info">
				<a className="product-title">
					{article.name}
					<span className="label label-danger pull-right">{article.price}</span>
				</a>
				<span className="product-description">
					{article.labels.map((id) => <Label key={id} labelID={id} />)}
				</span>
			</div>
		</li>)
	}

	render() {
		return (
			<div className="box">
				<div className="box-header with-border">
					<h3 className="box-title">Search Articles</h3>
					{
						this.props.toolButtons ? (
							<div className="box-tools">
								<div className="input-group">
									<div className="btn-group">
										{this.props.toolButtons}
									</div>
								</div>
							</div>
						) : null
					}
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
			articles,
			labels,
			labelTypes,
		}, state),
		articles: state.articles.articles || [],
	}),
)(ArticleSelector)
