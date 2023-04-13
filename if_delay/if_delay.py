from pysros.management import connect, sros
from pysros.exceptions import *
from pysros.pprint import Table, Padding
import sys
 
def check_delay(conn_obj):
    # Check delay on each interface and report operational delay (whether it is static or dynamic doesn't matter)
    # Output is a custom table formatted by the pprint.Table module from pysros
    if_state = conn_obj.running.get('/nokia-state:state/router[router-name="Base"]/interface')
    if_delay_rows = []
    for if_name in if_state.keys():
        if 'if-attribute' in if_state[if_name].keys():
            delay = if_state[if_name]['if-attribute']['delay'].data
            oper_delay = delay['operational'].data    
            if 'dynamic-measure' in delay.keys():
                dyn_delay = delay['dynamic-measure'].data
            else:
                dyn_delay = '-'
        else:
            dyn_delay = '-'
            oper_delay = '-'
        if_delay_rows.append([if_name, dyn_delay, oper_delay])
    if if_delay_rows:
        summary = 'A status of "-" means delay is not configured for that interface'
        if_col_hdr = [(20, 'Interface'), (20, 'Dynamic Delay'), (20, 'Operational Delay')]
        tbl_width = sum([col[0] for col in if_col_hdr])
        delay_table = Table('Interface delay measurements', 
                            columns = if_col_hdr, 
                            summary = summary, 
                            showCount = None, 
                            width = tbl_width)
        print_table(delay_table, if_delay_rows)
    

                       
def print_table(table, rows):
    table.print(rows)


def main():
    c = connect()
    check_delay(c)


if __name__ == "__main__":
    main()

