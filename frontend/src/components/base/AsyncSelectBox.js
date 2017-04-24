import React, { PropTypes } from "react";

export default class AsyncSelectBox extends React.Component {
	static propTypes = {
		placeholder: PropTypes.string,
		results: PropTypes.array.isRequired,
		onSelect: PropTypes.func,
		onSearch: PropTypes.func,
		query: PropTypes.string,
		id: PropTypes.string,
	};

	constructor() {
		super();
		this.state = {
			focused: false,
			selected: null,
		};
	}

	handleKeyEvent(evt) {
		console.log(evt.key);
		if (this.state.selected !== null) {
			if (evt.key === 'Enter') {
				evt.preventDefault();
				this.props.onSelect(this.props.results[this.state.selected].key);
			} else if (evt.key === 'ArrowDown') {
				evt.preventDefault();
				this.setState(state => ({selected: Math.min(state.selected + 1, this.props.results.length - 1)}))
			} else if (evt.key === 'ArrowUp') {
				evt.preventDefault();
				this.setState(state => ({selected: Math.max(state.selected - 1, 0)}));
			}
		} else if (this.props.results) {
			const amt = this.props.results.length;
			if (evt.key === 'ArrowUp') {
				this.setState({selected: amt - 1});
			} else if (evt.key === 'ArrowDown') {
				this.setState({selected: 0});
			} else if (evt.key === 'Enter' && amt === 1) {
				this.props.onSelect(this.props.results[0].key)
			}
		}
	}

	componentWillReceiveProps(props) {
		if (props.results && this.state.selected !== null && props.results.length < this.state.selected) {
			this.setState({selected: props.results.length});
		}
	}

	render() {
		return (
			<div
				onKeyDown={evt => this.handleKeyEvent(evt)}
				style={{ display: 'flex', flexDirection: 'column' }}>
				<input
					id={this.props.id}
					type="text"
					className="form-control"
					onChange={e => this.props.onSearch(e.target.value)}
					onFocus={() => this.setState({ focused: true })}
					onBlur={() => this.setState({ focused: false })}
					placeholder={this.props.placeholder}
					value={this.props.query} />
				<div className={"async-select-box-results-wrapper" + (this.state.focused ? ' async-select-box-results-wrapper-visible' : '')}>
					<div className="async-select-box-results">
						{this.props.results && this.props.results.length > 0 ? this.props.results.map(
							(result, index) =>
								<div className={index === this.state.selected ? 'selected' : ''} key={result.key} onClick={() => this.props.onSelect(result.key)}>
									<span>{result.label}</span>
								</div>
							) : <div>
							<span>No results</span>
						</div>}
					</div>
				</div>
			</div>
		);
	}
}
