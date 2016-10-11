/**
 * Created by Matthias on 11/10/2016.
 */

class MoneyColumn extends Column {
  constructor(key, name, currency) {
    if (name != null && name !== "") {
      name = `Cost (${currency.iso})`;
    }
    super(key, name);
  }
}