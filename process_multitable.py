import json

def json2list(table_rows, table_cols, cells):
    table_contents = [['' for c_i in range(table_cols)] for c_j in range(table_rows)]
    for cell in cells:
        cell_row = int(cell['start_row'])
        cell_col = int(cell['start_col'])
        table_contents[cell_row][cell_col] = cell['text']
    
    return table_contents

def json2list_multi(table_rows, table_cols, cells):
    table_contents = [['' for c_i in range(table_cols)] for c_j in range(table_rows)]
    header_flag = 1
    for cell in cells:
        start_row, start_col, end_row, end_col = int(cell['start_row']), int(cell['start_col']), int(cell['end_row']), int(cell['end_col'])
        if start_row == 0 and start_col == 0:
            header_flag = end_row - start_row + 1

        if start_row == end_row and start_col == end_col:
            table_contents[start_row][start_col] = cell['text']
            continue
        for r_i in range(start_row, end_row + 1):
            for c_i in range(start_col, end_col + 1):
                table_contents[r_i][c_i] = cell['text']   
    return table_contents, header_flag

def get_titile_and_unit(lines, position):
    title = ''
    unit = ''
    text_proposals = []
    for line in lines:
        text_position = line['position']
        if abs(text_position[5] - position[1]) > 200: continue
        text_proposals.append(line['text'])
        # print(f"pos: {position} vs text_pos: {text_position} vs text: {line['text']}")
        
    for text_proposal in text_proposals:
        if '适用' in text_proposal: continue
        if '单位:' in text_proposal: unit = text_proposal
        else: title = text_proposal
    
    return title, unit


def simple_table(tables):
    results = []
    last_text = None
    for i in range(len(tables)):
        table_dict = {
            'title': '',
            'unit': '',
            'header': '',
            'key_index': '',
            'values': ''
        }
        type_ = tables[i]['type']
        if 'table' not in type_:
            last_text = tables[i]
            continue

        position = tables[i]['position']
        table_rows = tables[i]['table_rows']
        table_cols = tables[i]['table_cols']
        cells = tables[i]['table_cells']
        
        table_contents, header_flag = json2list_multi(table_rows, table_cols, cells)

        header = []
        key_index = []
        values = []
        if header_flag == 1:
            header = table_contents[0]
        else:
            header = table_contents[0:header_flag]

        for t_i in range(header_flag, len(table_contents)):
            key_index.append(table_contents[t_i][0])
            values.append(table_contents[t_i][1:])

        table_dict['header'] = header
        table_dict['key_index'] = key_index
        table_dict['values'] = values

        table_dict['title'], table_dict['unit'] = get_titile_and_unit(last_text['lines'], position)

        results.append(table_dict)
    
    return results

if __name__ == "__main__":
    with open("C:/Users/wendy/Desktop/annual_report.json", 'r',encoding='utf-8') as f:
        j_f = json.load(f)

    tables = j_f['062.png'][0]['result']['tables']
    results = simple_table(tables)
    for result in results:
        print(f"{result}\n")
        