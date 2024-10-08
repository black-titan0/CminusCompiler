from .runtime_memory import *
from .semantic_stack import SemanticStack

LINE_SIZE = 40


class CodeGenerator:
    def __init__(self, parser) -> None:
        memory = Memory(0, 512, 1000)
        self.parser = parser
        self.semantic_errors = {}
        self.memory = memory
        self.semantic_stack = SemanticStack()
        self.program_block = memory.PB
        self.data_block = memory.DB
        self.temp_block = memory.TB
        self.global_symbol_table = {}
        self.current_symbol_table = self.global_symbol_table
        self.all_symbol_tables = {'global': self.global_symbol_table}
        self.call_stack = []
        self.function_stack_pointer = 4000
        self.top_sp = 500
        self.STACK_PLACE = 5000

    def function_call_instructions(self, function_object: Data, ar_size, arguments):
        self.push_function_stack(self.top_sp)

        function_symbol_table = self.all_symbol_tables[function_object.lexeme]
        self.call_stack.append(self.current_symbol_table)
        self.current_symbol_table = function_symbol_table
        start_index_of_ar = self.memory.TB.get_temp()
        self.memory.PB.add_instruction(Instruction('ADD', self.top_sp, f'#{ar_size}', start_index_of_ar))
        for i, argument in enumerate(arguments):
            argument_name = list(function_symbol_table.keys())[i]
            temp_for_arg_address_in_new_ar = self.memory.TB.get_temp()
            is_global_or_main, offset, data = self.get_data_by_name(argument_name)
            self.memory.PB.add_instruction(Instruction('ADD', start_index_of_ar, f'#{offset}',
                                                       temp_for_arg_address_in_new_ar))

            if data.type == 'array':
                if str(argument).startswith('@'):
                    temp = self.memory.TB.get_temp()
                    self.memory.PB.add_instruction(Instruction('ASSIGN', argument, temp, ''))
                    self.memory.PB.add_instruction(Instruction('ASSIGN',
                                                               temp,
                                                               f'@{temp_for_arg_address_in_new_ar}', ''))
                else:
                    self.memory.PB.add_instruction(Instruction('ASSIGN',
                                                               f'#{argument}',
                                                               f'@{temp_for_arg_address_in_new_ar}', ''))
            else:
                self.memory.PB.add_instruction(Instruction('ASSIGN',
                                                           argument,
                                                           f'@{temp_for_arg_address_in_new_ar}', ''))

        self.memory.PB.add_instruction(Instruction('ADD', self.top_sp, f'#{ar_size}', self.top_sp))
        temp = self.memory.TB.get_temp()
        self.memory.PB.add_instruction(Instruction('ADD', self.top_sp, f'#{INT_SIZE}', temp))
        self.memory.PB.add_instruction(Instruction('ASSIGN', f'#{self.memory.PB.current_index + 3}', f'@{temp}', ''))

        return_value_temp = self.memory.TB.get_temp()
        self.memory.PB.add_instruction(Instruction('ASSIGN', f'#{return_value_temp}', f'@{self.top_sp}', ''))

        self.memory.PB.add_instruction(Instruction('JP', function_object.address, '', ''))
        self.current_symbol_table = self.call_stack.pop()
        return return_value_temp

    def do_types_match(self, first_operand, second_operand):
        first_type = 'int'
        second_type = 'int'
        try:
            address = int(first_operand)
            first_type = self.memory.DB.block[address].type
        except:
            first_type = 'int'
        try:
            address = int(second_operand)
            second_type = self.memory.DB.block[address].type
        except:
            second_type = 'int'
        # return first_type, second_type, first_type == second_type
        return first_type, second_type, True

    def save_token_in_semantic_stack(self, current_token):
        self.semantic_stack.push(current_token[1])

    def save_number_in_semantic_stack(self, current_token):
        self.semantic_stack.push('#' + current_token[1])

    def declare_variable(self, current_token):
        name = self.semantic_stack.pop()
        data_type = self.semantic_stack.pop()
        if data_type == 'void':
            self.semantic_errors[int(self.parser.scanner.get_line_number()) - 1] = \
                "Semantic Error! Illegal type of void for '" + name + "'"
            self.memory.PB.has_error = True
        else:
            self.data_block.create_data(name, 'int', self.current_symbol_table)

    def declare_array(self, current_token):
        array_size = self.semantic_stack.pop()
        name = self.semantic_stack.pop()
        self.data_block.create_data(name, 'array', self.current_symbol_table, int(array_size),
                                    {'array_size': int(array_size)})

    def get_data_by_name(self, name):
        if name in self.current_symbol_table:
            offset = self.current_symbol_table[name].address - \
                     self.current_symbol_table[list(self.current_symbol_table.keys())[0]].address + 2 * INT_SIZE
            is_global_or_main = 'main' in self.all_symbol_tables and \
                                self.all_symbol_tables['main'] == self.current_symbol_table
            return is_global_or_main, offset, self.current_symbol_table[name]
        elif name in self.global_symbol_table:
            return True, 0, self.global_symbol_table[name]
        else:
            raise Exception("name not found!")

    def find_address_and_save(self, current_token, should_save=True):
        name = current_token[1]
        if name == 'output':
            self.semantic_stack.push('PRINT')
            return

        try:
            is_global_or_main, offset, datum = self.get_data_by_name(name)
            address = datum.address
            if not is_global_or_main:
                address = self.memory.TB.get_temp()
                self.memory.PB.add_instruction(
                    Instruction('ADD', self.top_sp, f'#{offset}', address)
                )
                self.semantic_stack.push(f'@{address}')
                return
            self.semantic_stack.push(address)
        except Exception as e:
            self.semantic_errors[int(self.parser.scanner.get_line_number())] = \
                self.semantic_errors.get(int(self.parser.scanner.get_line_number()), '') + "Semantic Error! '" \
                + name + \
                "' is not defined." + "*******"
            self.semantic_stack.push(-1)
            self.memory.PB.has_error = True

    def multiply(self, current_token):
        temp = self.temp_block.get_temp()
        second = self.semantic_stack.pop()
        first = self.semantic_stack.pop()
        first_type, second_type, match = self.do_types_match(first, second)
        if match:
            instruction = Instruction('MULT', first, second, temp)
            self.semantic_stack.push(temp)
            self.program_block.add_instruction(instruction)
        else:
            self.semantic_errors[int(self.parser.scanner.get_line_number())] = \
                f"Semantic Error! Type mismatch in operands, Got array instead of int."
            self.semantic_stack.push(temp)
            self.memory.PB.has_error = True

    def add_or_subtract(self, current_token):
        temp = self.temp_block.get_temp()
        second_operand = self.semantic_stack.pop()
        op = self.semantic_stack.pop()
        first_operand = self.semantic_stack.pop()
        if op == '+':
            op = 'ADD'
        elif op == '-':
            op = 'SUB'
        first_type, second_type, match = self.do_types_match(first_operand, second_operand)
        if match:
            instruction = Instruction(op, first_operand, second_operand, temp)
            self.semantic_stack.push(temp)
            self.program_block.add_instruction(instruction)
        else:
            self.semantic_errors[int(self.parser.scanner.get_line_number())] = \
                f"Semantic Error! Type mismatch in operands, Got {second_type} instead of {first_type}."
            self.semantic_stack.push(temp)
            self.memory.PB.has_error = True

    def compare(self, current_token):
        temp = self.temp_block.get_temp()
        second_operand = self.semantic_stack.pop()
        op = self.semantic_stack.pop()
        first_operand = self.semantic_stack.pop()
        if op == '<':
            op = 'LT'
        elif op == '==':
            op = 'EQ'
        first_type, second_type, match = self.do_types_match(first_operand, second_operand)
        if match:
            instruction = Instruction(op, first_operand, second_operand, temp)
            self.semantic_stack.push(temp)
            self.program_block.add_instruction(instruction)
        else:
            self.semantic_errors[int(self.parser.scanner.get_line_number())] = \
                f"Semantic Error! Type mismatch in operands, Got {second_type} instead of {first_type}."
            self.semantic_stack.push(temp)
            self.memory.PB.has_error = True

    def label(self, current_token):
        idx = self.program_block.current_index
        self.semantic_stack.push(idx)

    def repeat_until_iter(self, current_token):
        temp = self.semantic_stack.pop()
        print(self.semantic_errors)
        while type(self.semantic_stack.top()) == str or self.semantic_stack.top() >= self.memory.DB.base:
            self.semantic_stack.pop()
        instr = Instruction('JPF', temp, self.semantic_stack.top(), '')
        self.program_block.add_instruction(instr)
        self.semantic_stack.pop()

        # handle break
        program_block = self.memory.PB
        for address in program_block.block:
            instruction = program_block.block[address]
            if type(instruction) == tuple and instruction[0] == 'break':
                if instruction[1] == program_block.scope + 1:
                    new_instr = Instruction('JP', self.program_block.current_index, '', '')
                    program_block.add_instruction(new_instr, address)

    def save_pb_index(self, current_token):
        idx = self.program_block.current_index
        self.semantic_stack.push(idx)
        self.program_block.increase_index()

    def jpf_save(self, current_token):
        idx = self.program_block.current_index
        while type(self.semantic_stack.top()) == str or self.semantic_stack.top() >= self.memory.DB.base:
            self.semantic_stack.pop()
        address = self.semantic_stack.pop()
        instr = Instruction('JPF', self.semantic_stack.top(), idx + 1, '')
        self.program_block.add_instruction(instr, address)
        self.semantic_stack.pop()
        self.semantic_stack.push(idx)
        self.program_block.increase_index()

    def jp(self, current_token):
        idx = self.program_block.current_index
        instr = Instruction('JP', idx, '', '')
        while type(self.semantic_stack.top()) == str or self.semantic_stack.top() >= self.memory.DB.base:
            self.semantic_stack.pop()
        self.program_block.add_instruction(instr, self.semantic_stack.top())
        self.semantic_stack.pop()

    def assign(self, current_token):
        instr = Instruction('ASSIGN', self.semantic_stack.pop(), self.semantic_stack.top(), '')
        self.program_block.add_instruction(instr)

    def print_instruction(self, current_token):
        if not self.semantic_stack.is_empty() and self.semantic_stack.top(1) == 'PRINT':
            operand = self.semantic_stack.pop()
            instr = Instruction(self.semantic_stack.pop(), operand, '', '')
            self.program_block.add_instruction(instr)

    def calculate_array_address(self, current_token):
        temp = self.temp_block.get_temp()
        temp2 = self.temp_block.get_temp()
        offset = self.semantic_stack.pop()
        base = self.semantic_stack.pop()
        mult_instruction = Instruction('MULT', '#4', offset, temp)
        self.program_block.add_instruction(mult_instruction)
        if str(base).startswith('@'):
            temp_array_base = self.temp_block.get_temp()
            self.program_block.add_instruction(Instruction('ASSIGN', base, temp_array_base, ''))
            add_instruction = Instruction('ADD', temp_array_base, temp, temp2)
        else:
            add_instruction = Instruction('ADD', '#' + str(base), temp, temp2)
        self.program_block.add_instruction(add_instruction)
        self.semantic_stack.push('@' + str(temp2))

    def end_scope(self, current_token):
        self.memory.PB.dec_scope()

    def begin_scope(self, current_token):
        self.memory.PB.inc_scope()

    def save_break(self, current_token):
        if self.memory.PB.scope > 0:
            self.program_block.add_instruction(('break', self.memory.PB.scope))
        else:
            line_number = int(self.parser.scanner.get_line_number()) - 1
            if line_number == LINE_SIZE and current_token[1] == 'if': line_number -= 1
            self.semantic_errors[line_number] = \
                "Semantic Error! No 'repeat ... until' found for 'break'."
            self.memory.PB.has_error = True

    def declare_function(self, current_token):
        name = self.semantic_stack.pop()
        if name == 'main':
            self.memory.PB.add_instruction(Instruction('ASSIGN', '#10000',
                                                       self.memory.DB.base - INT_SIZE, ''),
                                           self.memory.PB.base)
            self.memory.PB.add_instruction(Instruction('ASSIGN', '#10000',
                                                       self.STACK_PLACE - INT_SIZE, ''),
                                           self.memory.PB.base + 1)
            self.memory.PB.add_instruction(Instruction('ASSIGN', f'#{self.STACK_PLACE}',
                                                       self.function_stack_pointer, ''),
                                           self.memory.PB.base + 2)
            self.memory.PB.add_instruction(Instruction('ASSIGN', f'#{self.top_sp + INT_SIZE}', self.top_sp, ''),
                                           self.memory.PB.base + 3)
            self.memory.PB.add_instruction(Instruction('JP', self.memory.PB.current_index, '', ''),
                                           self.memory.PB.base + 4)
        data_type = self.semantic_stack.pop()
        self.current_symbol_table = {}
        self.global_symbol_table[name] = Data(name, data_type, self.memory.PB.current_index, True)
        self.all_symbol_tables[name] = self.current_symbol_table
        self.semantic_stack.push(name)

    def end_function(self, current_token):
        self.current_symbol_table = self.global_symbol_table
        self.return_jump(current_token)

    def declare_pointer(self, current_token):
        name = self.semantic_stack.pop()
        data_type = self.semantic_stack.pop()
        if data_type == 'void':
            self.semantic_errors[int(self.parser.scanner.get_line_number()) - 1] = \
                "Semantic Error! Illegal type of void for '" + name + "'"
            self.memory.PB.has_error = True
        else:
            self.data_block.create_data(name, 'array', self.current_symbol_table)

    def save_function_parameters_information(self, current_token):
        name = self.semantic_stack.pop()
        arg_types = []
        for datum_name in self.current_symbol_table:
            datum = self.current_symbol_table[datum_name]
            arg_types.append(datum.address)
        self.global_symbol_table[name].attrs['arguments'] = arg_types

    def check_function_args(self, current_token):
        if '#arguments' not in self.semantic_stack.stack:
            return
        args = []
        while self.semantic_stack.top() != '#arguments':
            arg = self.semantic_stack.pop()
            args.append(arg)
        args = list(reversed(args))
        self.semantic_stack.pop()
        if self.semantic_stack.top() == 'PRINT':
            self.semantic_stack.push(args[0])
            return
        address = self.semantic_stack.pop()
        func: Data = None
        for datum in self.global_symbol_table:
            if self.global_symbol_table[datum].address == address:
                func = self.global_symbol_table[datum]
                break

        func_args = func.attrs['arguments']
        # if len(args) != len(func_args):
        #     self.semantic_errors[int(self.parser.scanner.get_line_number())] = \
        #         f"Semantic Error! Mismatch in numbers of arguments of '{func.lexeme}'"
        #     self.memory.PB.has_error = True
        #     return
        #
        # for i in range(len(args)):
        #     given_type, func_arg_type, match = self.do_types_match(args[i], func_args[i])
        #     if not match:
        #         self.semantic_errors[int(self.parser.scanner.get_line_number())] = \
        #             f"Semantic Error! Mismatch in type of argument {i + 1} of '{func.lexeme}'. Expected " \
        #             f"'{func_arg_type}' but got '{given_type}' instead."
        #         self.memory.PB.has_error = True
        #         return
        ar_size = 2 * INT_SIZE
        if self.current_symbol_table:
            ar_size += self.current_symbol_table[list(self.current_symbol_table.keys())[-1]].address - \
                       self.current_symbol_table[list(self.current_symbol_table.keys())[0]].address + INT_SIZE
        if 'main' in self.all_symbol_tables and self.current_symbol_table == self.all_symbol_tables['main']:
            first_function = -1
            i = 0
            for symbol in self.global_symbol_table:
                if self.global_symbol_table[symbol].is_function:
                    first_function = i - 1
                    break
                i += 1
            last_global: Data = self.global_symbol_table[list(self.global_symbol_table.keys())[first_function]]
            last_global_address = last_global.address
            if last_global.type == 'array':
                last_global_address += (last_global.attrs['array_size'] - 1) * 4

            ar_size += last_global_address - \
                       self.global_symbol_table[list(self.global_symbol_table.keys())[0]].address
        return_value_temp = self.function_call_instructions(func, ar_size, args)
        self.semantic_stack.push(return_value_temp)
        pass

    def return_value(self, current_token):
        value = self.semantic_stack.pop()
        temp = self.memory.TB.get_temp()
        self.memory.PB.add_instruction(Instruction(
            'ASSIGN', f'@{self.top_sp}', temp, ''
        ))
        self.memory.PB.add_instruction(Instruction(
            'ASSIGN', value, f'@{temp}', ''
        ))
        self.return_jump(current_token)

    def return_jump(self, current_token):
        temp = self.memory.TB.get_temp()
        self.memory.PB.add_instruction(Instruction(
            'ADD', self.top_sp, f'#{INT_SIZE}', temp
        ))
        self.pop_function_stack()
        self.memory.PB.add_instruction(Instruction(
            'ASSIGN', f'@{temp}', temp, ''
        ))

        self.memory.PB.add_instruction(Instruction(
            'JP', f'@{temp}', '', ''
        ))

    def start_func_call_args(self, current_token):
        if self.semantic_stack.top() == 'PRINT':
            return
        self.semantic_stack.push('#arguments')

    def push_function_stack(self, addr):
        self.memory.PB.add_instruction(Instruction('ASSIGN', addr, f'@{self.function_stack_pointer}', ''))
        self.memory.PB.add_instruction(Instruction('ADD', f'#{INT_SIZE}', self.function_stack_pointer,
                                                   self.function_stack_pointer))

    def pop_function_stack(self):
        self.memory.PB.add_instruction(Instruction('SUB', self.function_stack_pointer, f'#{INT_SIZE}',
                                                   self.function_stack_pointer))
        self.memory.PB.add_instruction(Instruction('ASSIGN', f'@{self.function_stack_pointer}', self.top_sp, ''))
