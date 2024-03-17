import json

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
        if type_ == 'plain':
            last_text = tables[i]
        if 'table' not in type_:
            continue
        position = tables[i]['position']
        table_rows = tables[i]['table_rows']
        table_cols = tables[i]['table_cols']
        cells = tables[i]['table_cells']

        header = []
        key_index = []
        values = []

        table_contents = [['' for c_i in range(table_cols)] for c_j in range(table_rows)]
        for cell in cells:
            cell_row = int(cell['start_row'])
            cell_col = int(cell['start_col'])
            table_contents[cell_row][cell_col] = cell['text']

        header = table_contents[0]
        for t_i in range(1, len(table_contents)):
            key_index.append(table_contents[t_i][0])
            values.append(table_contents[t_i][1:])

        table_dict['header'] = header
        table_dict['key_index'] = key_index
        table_dict['values'] = values

        lines = last_text['lines']
        text_proposals = []
        for line in lines:
            text_position = line['position']
            if abs(text_position[5] - position[1]) > 200: continue
            text_proposals.append(line['text'])
            # print(f"pos: {position} vs text_pos: {text_position} vs text: {line['text']}")
        
        for text_proposal in text_proposals:
            if '适用' in text_proposal: continue
            if '单位:' in text_proposal: table_dict['unit'] = text_proposal
            else: table_dict['title'] = text_proposal

        results.append(table_dict)
    
    return results

if __name__ == "__main__":
    with open("C:/Users/wendy/Desktop/annual_report.json", 'r',encoding='utf-8') as f:
        j_f = json.load(f)
    tables = j_f['009.png'][0]['result']['tables']
    results = simple_table(tables)
    for result in results:
        print(f"{result}\n")
        