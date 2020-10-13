from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient(host="10.162.0.111", port=502)


def get_input():
    return client.read_input_registers(0).registers[0]


def get_now_state():
    # Тут делается дважды одно и тоже
    # Нужно разобраться что лишнее!
    b = [False] * 9
    On = client.read_holding_registers(1).registers[0]
    On = bin(On)
    k = 0
    i = len(On) - 1
    while i > 1:
        if On[i] == '1':
            b[k] = True
        k += 1
        i -= 1

    On = client.read_holding_registers(1).registers[0]
    On = bin(On)
    k = 0
    for i in range(len(On), 2):
        if On[i] == '1':
            b[k] = True
        k += 1
    return b


def get_tool_outputs():
    value = [False] * 2
    # Тут делается дважды одно и тоже
    # Нужно разобраться что лишнее!
    On = client.read_holding_registers(22).registers[0]
    On = bin(On)
    k = 0
    i = len(On) - 1
    while i > 1:
        if On[i] == '1':
            value[k] = True
        k += 1
        i -= 1

    On = client.read_holding_registers(1).registers[0]
    On = bin(On)
    k = 0
    for i in range(len(On), 2):
        if On[i] == '1':
            value[k] = True
        k += 1
    return value


def set_output(num):
    b = get_now_state()
    if num < 0:
        client.write_register(1, 0)
        return 1

    if not b[num]:
        On = client.read_holding_registers(1).registers[0]
        b[num] = True
        num = 2 ** num
        On += num
        client.write_register(1, On)
    else:
        On = client.read_holding_registers(1).registers[0]
        b[num] = False
        num = 2 ** num
        On -= num
        client.write_register(1, abs(On))
    return 1


def set_tool_output(num):
    b = get_tool_outputs()
    if num < 0:
        client.write_register(22, 0)
        return 1

    if not b[num]:
        On = client.read_holding_registers(22).registers[0]
        b[num] = True
        num = 2 ** num
        On += num
        client.write_register(22, On)
    else:
        On = client.read_holding_registers(22).registers[0]
        b[num] = False
        num = 2 ** num
        On -= num
        client.write_register(22, abs(On))
    return 1
