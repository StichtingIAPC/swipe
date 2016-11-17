/**
 * Created by Matthias on 06/11/2016.
 */

class Auth {
  constructor() {
    this._user = null;
  }

  login({username, password}) {
    return new Promise((accept, reject) => {
      if (this._user !== null)
        reject(`User is already logged in: ${this._user.username}`);
      if (Math.random() > 0.8) {
        this._user = {
          username: username,
        };
        accept({});
      } else {
        reject('Math.random() <= 0.8');
      }
    })
  }

  logout() {
    return new Promise((accept, reject) => {
      this._user = null;
      accept();
    })
  }

  get username() {
    if (this._user !== null)
      return this._user.username;
    return '';
  }

  getUser() {
    return this._user;
  }

  isLoggedIn(username=null) {
    if (username !== null) {
      if (this._user !== null)
        return this._user.username == username;
      return false;
    }
    return this._user !== null;
  }
}

export default new Auth();
