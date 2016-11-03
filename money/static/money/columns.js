import { Column } from "js/tools/tables"

export class MoneyColumn extends Column {
  constructor({key, name, currency}) {
    if (name != null && name !== "") {
      name = `Cost (${currency.iso})`;
    }
    super({key, name});
  }
}