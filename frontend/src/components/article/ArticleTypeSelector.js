import React, { Component } from 'react';
import Select from 'react-select';
import { connect } from 'react-redux';
import { fetchAllArticles } from '../../state/assortment/articles/actions';

export class ArticleTypeSelector extends Component {
	constructor(props) {
		super(props);
		this.state = {
			articleTypes: [],
		};
	}

	componentDidMount() {
		this.props.fetchArticleTypes();
		this.componentWillReceiveProps(this.props);
	}

	changeType = option => {
		if (!option) {
			this.props.onChange(null);
			return;
		}
		const article = this.props.articleTypes.filter(t => t.id === option.value)[0];

		if (this.props.onChange instanceof Function) {
			this.props.onChange(article);
		}
	};

	componentWillReceiveProps(props) {
		this.setState({
			articleTypes: props.articleTypes.map(type => ({
				value: type.id,
				label: type.name,
			})),
		});
	}

	render() {
		return <Select
			name={this.props.name}
			options={this.state.articleTypes}
			value={this.props.value }
			onChange={this.changeType} />;
	}
}

export default connect(
	state => ({
		articleTypes: state.assortment.articles.articles,
	}),
	{
		fetchArticleTypes: fetchAllArticles,
	}
)(ArticleTypeSelector);
