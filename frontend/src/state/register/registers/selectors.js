export const getActiveRegisters = (state) => state.register.registers.registers.filter(register => register.is_active);
