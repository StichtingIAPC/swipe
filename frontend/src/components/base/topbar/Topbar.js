import React from 'react';
import PropTypes from 'prop-types';
import UserBlock from './UserBlock';

export class Topbar extends React.Component {
	render() {
		return (
			<header className="main-header">
				<a className="logo">
					<span className="logo-mini">👆ミ</span>
					<span className="logo-lg">Swipe</span>
				</a>
				<nav className="navbar navbar-static-top" role="navigation">
					<a className="sidebar-toggle" onClick={this.props.sidebarToggle} />
					<div className="navbar-custom-menu pull-left">
						<ul className="nav navbar-nav">
							<li>
								<a>{this.props.name}</a>
							</li>
						</ul>
					</div>
					<div className="navbar-custom-menu">
						<ul className="nav navbar-nav">
							<UserBlock />
						</ul>
					</div>
				</nav>
			</header>
		);
	}
}

Topbar.propTypes = {
	sidebarToggle: PropTypes.func.isRequired,
	name: PropTypes.string,
};

Topbar.defaultProps = { name: 'page' };

export default Topbar;
