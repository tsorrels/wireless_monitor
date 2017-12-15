import curses


class Controller(object):
    def __init__(self, display, state):

        self.__operations = { }        
        self.__populate_core_operations()
        self.display = display
        self.state = state
        self.__map_extensions()

    def __populate_core_operations(self):

        self.__operations[ord('r')] = self.__remove
        self.__operations[ord('q')] = self.__quit
        self.__operations[ord('p')] = self.__toggle_pause
        self.__operations[curses.KEY_UP] = self.__move_up
        self.__operations[curses.KEY_DOWN] = self.__move_down
                       

    def __map_extensions(self):

        for cmd in self.state.cmd_extensions:
            if cmd.key in self.__operations:
                #TODO: return error, key can only be mapped once
                continue
            
            self.__operations[ord(cmd.key)] = cmd.function

        

    def do_operation(self, input, data):
        # edge case where data is an empty row
        # can result when user removes bottom connection
        if not data:
            pass
        try:
            self.__operations[input](data, self.state)

        except KeyError as e:
            self.state.logwriter.write('error', 'invalid input:' + str(input)
                                       +'\n')
            # TODO: return false to identify bad input
            pass


    def __move_up(self, data, state):
        with state.all_lock:       
            if self.display.cur_row  > self.display.num_header_rows:
                self.display.cur_row -= 1
                self.display.cur_index -= 1


            elif self.display.cur_row == self.display.num_header_rows and \
                 self.display.cur_index > 0:
                self.display.cur_index -= 1
                self.display.win_start_index -= 1
            
        self.display.display()

    def __move_down(self, data, state):
        with state.all_lock:

            #state.logwriter.write('error', str(self.display.scr_dimensions[0]))
            if self.display.cur_row < self.display.scr_dimensions[0] and \
               self.display.cur_index < len(state.all_connections) - 1:
                self.display.cur_row += 1
                self.display.cur_index += 1
            
            elif self.display.cur_row == self.display.scr_dimensions[0] and \
                 self.display.cur_index < len(state.all_connections):
                self.display.cur_index += 1
                self.display.win_start_index += 1

            else:
                stringVar = 'cur_index = {0}, cur_row = {1}, win_start_index = {2}\n'.format(self.display.cur_index, self.display.cur_row, self.display.win_start_index)
                state.logwriter.write('error', stringVar)

                
        self.display.display()

        
    def __toggle_pause(self, data, state):
        pass


    def __quit(self, data, state):
        # TODO: call quit/cleanup for all modules
        for function in state.exit_functions:
            function(self.state)
        curses.endwin()
        exit(0)
        

    def __remove(self, data, state):
        # check edge case
        if len(state.all_connections) == 0:
            return

        self.state.logwriter.write('error', 'ran __remove\n')
        connection = self.state.find_connection(data)
        if connection:
            with self.state.all_lock:
                self.state.all_connections.remove(connection)

        # check if user removed the last connection in list
        if self.display.cur_index == len(state.all_connections):
            self.display.cur_index = len(state.all_connections) - 1
            self.display.cur_row -= 1

        # check if that was the only connection
        if len(state.all_connections) == 0:
            # reset 
            self.cur_row = 1
            self.cur_index = 0
            self.win_start_index = 0
            self.num_output_rows = 0
