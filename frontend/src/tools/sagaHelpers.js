export const cleanErrorMessage = error => {
	if (error instanceof Error) {
		return error.message;
	} else if (error instanceof Object) {
		return error;
	}
	return null;
};
