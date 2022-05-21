import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks/312464#312464
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def find_first(lst):
    ctr = 0
    for idx, data in enumerate(lst):
        if ctr == 3:
            if data[1] > 0:
                if idx - 15 > -1 and lst[idx-15][1] > 0:
                    return idx - 15
                else:
                    ctr = 0
            else:
                ctr = 0
        elif data[1] < 0:
            ctr += 1
        else:
            ctr = 0

wrongs = []
times = []
datas = []
with open(args.filename, 'r') as f:
    splited = [data.split() for data in f.read().splitlines()[1:]]
    floated = [[float(x), float(y)] for x, y in splited]
    packets = [packet for packet in chunks(floated, 16)]
    ref = 5/1024
    for packet in packets:
        time =  packet[0][0]
        data = 0
        ones = 0
        for idx, bit in enumerate(packet[10:0:-1]):
            if bit[1] > 0:
                data |= 0x1 << idx
                ones += 1
        data = (data*ref) - 2.5
        if ones % 2:
            correct_par = 5
        else:
            correct_par = -5
        if correct_par != packet[11][1]:
            wrongs.append(time)
        times.append(time)
        datas.append(data)
