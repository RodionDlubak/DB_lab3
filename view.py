from tabulate import tabulate


class View:
    def print(self, table_name, data):
        arr = [];
        columns = [' ', ' ', ' ', ' ']
        if table_name == 'account':
            for r in data:
                arr.append([r.account_id, r.login, r.password, r.created])
            print(tabulate(arr, headers=columns, tablefmt='orgtbl'))

        if table_name == 'game':
            for r in data:
                arr.append([r.game_id, r.game_name, r.hours_played, r.account])
            print(tabulate(arr, headers=columns, tablefmt='orgtbl'))

        if table_name == 'item':
            for r in data:
                arr.append([r.item_id, r.item_name, r.price, r.game])
            print(tabulate(arr, headers=columns, tablefmt='orgtbl'))
