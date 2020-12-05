from consolemenu import SelectionMenu
from model import Model
from view import View

TABLES_NAMES = ['account', 'game', 'item']
TABLES = {
'account': ['account_id', 'login', 'password', 'created'],
'game': ['game_id', 'game_name', 'hours_played', 'account'],
'item': ['item_name', 'price', 'game', 'item_id']
}


def getInput(msg, tableName=''):
    print(msg)
    if tableName:
        print(' | '.join(TABLES[tableName]), end='\n\n')
    return input()


def getInsertInput(msg, tableName):
    print(msg)
    print(' | '.join(TABLES[tableName]), end='\n\n')
    return input(), input()


def pressEnter():
    input()



class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def show_main_menu(self, msg=''):
        menu = SelectionMenu(
            TABLES_NAMES + ['Fill table "account" by random data (10 000 items)', 'Commit'],
            title='Select the table to work with | command:', subtitle=msg)
        menu.show()

        index = menu.selected_option
        if index < len(TABLES_NAMES):
            table_name = TABLES_NAMES[index]
            self.show_entity_menu(table_name)
        elif index == len(TABLES_NAMES):
            self.fill_by_random()
        elif index == len(TABLES_NAMES) + 1:
            self.model.commit()
            self.show_main_menu(msg='Commit successful')
        else:
            print('Bye')

    def show_entity_menu(self, table_name, msg=''):
        options = ['Get', 'Delete', 'Update', 'Insert']
        functions = [self.get, self.delete, self.update, self.insert]

        selection_menu = SelectionMenu(options, f'Name of table: {table_name}',
                                       exit_option_text='Back', subtitle=msg)
        selection_menu.show()
        try:
            function = functions[selection_menu.selected_option]
            function(table_name)
        except IndexError:
            self.show_main_menu()

    def get(self, table_name):
        try:
            condition = getInput(
                f'GET {table_name}\nEnter condition (SQL) or leave empty:', table_name)
            data = self.model.get(table_name, condition)
            self.view.print(table_name, data)
            pressEnter()
            self.show_entity_menu(table_name)
        except Exception as err:
            self.show_entity_menu(table_name, str(err))

    def insert(self, table_name):
        try:
            columns, values = getInsertInput(
                f"INSERT {table_name}\nEnter columns divided with commas, then do the same for values in format: [value1, value2, ...]",
                table_name)
            self.model.insert(table_name, columns, values)
            self.show_entity_menu(table_name, 'Insert is successful!')
        except Exception as err:
            self.show_entity_menu(table_name, str(err))

    def delete(self, table_name):
        try:
            condition = getInput(
                f'DELETE {table_name}\n Enter condition (SQL):', table_name)
            self.model.delete(table_name, condition)
            self.show_entity_menu(table_name, 'Delete is successful')
        except Exception as err:
            self.show_entity_menu(table_name, str(err))

    def update(self, table_name):
        try:
            condition = getInput(
                f'UPDATE {table_name}\nEnter condition (SQL):', table_name)
            statement = getInput(
                "Enter SQL statement in format [<key>=<value>]", table_name)

            self.model.update(table_name, condition, statement)
            self.show_entity_menu(table_name, 'Update is successful')
        except Exception as err:
            self.show_entity_menu(table_name, str(err))

    def fill_by_random(self):
        try:
            self.model.fill_account_with_random_data()
            self.show_main_menu('10 000 accounts were generated successfully')
        except Exception as err:
            self.show_main_menu(str(err))