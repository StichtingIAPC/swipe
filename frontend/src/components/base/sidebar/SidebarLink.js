import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import FontAwesome from '../../tools/icons/FontAwesome.js';

export default class SidebarLink extends React.Component {
	constructor(props) {
		super(props);
		this.state = { open: null };
	}

	toggle(evt) {
		this.setState({ open: this.state.open ? null : 'active' });
		evt.preventDefault();
	}

	render() {
		const children = this.props.children ? (
			<ul className={`treeview-menu${this.state.open ? ' menu-open' : ''}`}>
				{this.props.children}
			</ul>
		) : null;

		const openswitch = this.props.children ? (
			<span className="pull-right-container" onClick={::this.toggle}>
				<FontAwesome icon={`${this.state.open ? 'minus-square' : 'plus-square'} pull-right`} />
			</span>
		) : null;

		if (this.props.to) {
			return (
				<li className={this.state.open ? 'treeview active' : 'treeview'}>
					<Link to={this.props.to} onClick={this.props.onClick} activeClassName={this.props.activeClassName}>
						<FontAwesome icon={this.props.icon} />
						<span>{this.props.text}</span>
						{this.props.indicator}
						{openswitch}
					</Link>
					{children}
				</li>
			);
		}
		return (
			<li className={this.state.open ? 'treeview active' : 'treeview'}>
				<a onClick={this.props.onClick}>
					<FontAwesome icon={this.props.icon} />
					<span>{this.props.text}</span>
					{this.props.indicator}
					{openswitch}
				</a>
				{children}
			</li>
		);
	}
}

SidebarLink.propTypes = {
	text: PropTypes.string.isRequired,
	to: PropTypes.string,
	icon: PropTypes.string,
	children: PropTypes.node,
	activeClassName: PropTypes.string,
	indicator: PropTypes.element,
};

SidebarLink.defaultProps = {
	icon: 'circle-o',
	activeClassName: 'active',
};
