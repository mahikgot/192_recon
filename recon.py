import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks/312464#312464
def chunks(lst):
    #yield valid packets, checks for header and footer bits
    i = 0
    while i < len(lst) - 15:
        chunk = lst[i:i + 16]
        if (chunk[0][1] > 0) and all(x[1] <= 0 for x in chunk[-4:-1]) and (chunk[-1][1] > 0):
            i += 16
            yield chunk
        else:
            i += 1

times = []
datas = []
with open(args.filename, 'r') as f:
    splited = [data.split() for data in f.read().splitlines()[1:]]
    floated = [[float(x), int(y)] for x, y in splited]
    packets = [packet for packet in chunks(floated)]
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

with open('output.txt', 'w') as f:
    for time, data in zip(times, datas):
        f.write(str(time) + ' ' + str(data) + '\n')
