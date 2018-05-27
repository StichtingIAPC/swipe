import React from 'react';
import { ThemeProvider } from 'styled-components';
import { darken } from 'polished';

export const theme = {
	font: {
		heading: 'Montserrat, sans-serif',
		body: 'Lato, sans-serif',
	},

	color: {
		black: '#2b2b2b',
		white: '#ffffff',
		primary: Object.assign('#4a90e2', {
			medium: darken(0.05, '#4a90e2'),
			dark: darken(0.1, '#4a90e2'),
		}),
		positive: {
			regular: '#2ecc71',
			medium: darken(0.05, '#2ecc71'),
			dark: darken(0.1, '#2ecc71'),
		},
		negative: {
			regular: '#e74c3c',
			medium: darken(0.05, '#e74c3c'),
			dark: darken(0.1, '#e74c3c'),
		},
		warning: {
			regular: '#f1c40f',
			medium: darken(0.05, '#f1c40f'),
			dark: darken(0.1, '#f1c40f'),
		},
	},

	spacing: 5,
};

const ThemeWrapper = ({ children }) => (
	<ThemeProvider theme={theme}>{children}</ThemeProvider>
);

export default ThemeWrapper;
