from pysros.management import connect, sros
from pysros.exceptions import *
from pysros.pprint import Table, Padding
import sys
 
def check_cpu(conn_obj):
    ## Get cpu info and show it in ascending order based on CPU Usage
    if_state = conn_obj.running.get('/nokia-state:state/system/cpu')
    # 1 second results
    if_cpu_rows = []
    if_state_1 = if_state[1].data
    for if_name in if_state_1.keys():
        if 'summary' in if_name:
            summary =  if_state_1[if_name].data
            idle_usage = summary['idle'].data
        elif 'sample-period' in if_name:
            sample =  if_state_1[if_name].data
            #print('sample: ', sample)
        else:      
            row_data = if_state_1[if_name].data
            #print(if_name,"  ",row_data['cpu-usage'])
            if_cpu_rows.append([if_name, row_data['cpu-usage']])
    if if_cpu_rows:
        bottom = "Idle Time: " + str(idle_usage['cpu-usage'])
        if_col_hdr = [(20, 'Name'), (20, 'CPU Usage')]
        tbl_width = sum([col[0] for col in if_col_hdr])
        cpu_table = Table('CPU Utilization (Sample period: 1 second)', 
                            columns = if_col_hdr, 
                            summary = bottom, 
                            showCount = None, 
                            width = tbl_width)
        print_table(cpu_table, sort_array(if_cpu_rows))

def print_table(table, rows):
    table.print(rows)

def sort_array(arr):
    return sorted(arr, key=lambda x: x[1], reverse=True)    

def main():
    c = connect()
    check_cpu(c)


if __name__ == "__main__":
    main()
