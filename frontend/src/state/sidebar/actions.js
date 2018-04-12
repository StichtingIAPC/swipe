export const SIDEBAR_TOGGLE = 'sidebar/toggle';
export const SIDEBAR_CLOSE = 'sidebar/close';
export const SIDEBAR_OPEN = 'sidebar/open';

export const toggleSidebar = () => ({
	type: SIDEBAR_TOGGLE,
});

export const closeSidebar = () => ({
	type: SIDEBAR_CLOSE,
});

export const openSidebar = () => ({
	type: SIDEBAR_OPEN,
});
