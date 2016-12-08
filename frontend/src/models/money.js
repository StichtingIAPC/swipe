import auth from "../core/auth";

/**
 * Created by Matthias on 27/11/2016.
 */

export class Model {
	constructor(url) {
		this._fields = null;
		this.fetchFields(url)
	}

	async fetchFields(url) {
		this._fields = auth.fetch(url, {
			method: 'OPTIONS',
		})
			.then((request) => request.json())
			.then((json) => json.actions.POST)
	}

	get fields() {
		if (!this._fields) {
			throw new Error('too early');
		}
		return this._fields;
	}
}
