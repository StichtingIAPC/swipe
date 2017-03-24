import React, { PropTypes } from 'react';

export default class AsyncSelectBox extends React.Component {
	static propTypes = {
		placeholder: PropTypes.string,
		results: PropTypes.array,
		onSelect: PropTypes.func,
		onSearch: PropTypes.func,
		query: PropTypes.string,
	};

	constructor() {
		super();
		this.state = { value: '', focused: false };
	}

	render() {
		return <div style={{ display: 'flex', flexDirection: 'column' }}>
			<input
				type="text"
				className="form-control"
				onChange={e => this.props.onSearch(e.target.value)}
				onFocus={() => this.setState({ focused: true })}
				onBlur={() => this.setState({ focused: false })}
				placeholder={this.props.placeholder}
				value={this.props.query} />
			<div className={"async-select-box-results-wrapper" + (this.state.focused ? ' async-select-box-results-wrapper-visible' : '')}>
				<div className="async-select-box-results">
					{this.props.results ? this.props.results.map(result => <div key={result.key} onClick={() => this.props.onSelect(result.key)}>
						<span>{result.label}</span>
					</div>) : <div>
						<span>No results</span>
					</div>}
				</div>
			</div>
		</div>;
	}
}
