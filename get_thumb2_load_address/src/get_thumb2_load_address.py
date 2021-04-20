import matplotlib.pyplot as plt
from multiprocessing import cpu_count
import time

#please set de guess load address range
#a lange range may cause a long time
guess_base_address_start = 0x20000
guess_base_address_end = 0x26010
acc = 4
guess_file_end = guess_base_address_start + bv.end

def do_find_disass(start_address,end_address):
    address_list = []
    fuction_start = {"ldr","push","b"}
    for ea in range(start_address, end_address, 4):
        disass = bv.get_disassembly(ea)
        if disass[0:(disass.find(" "))] in fuction_start:
            address_list.append(ea)
    print("disass serach over")
    return address_list

def do_find_point(start_adress,end_address):
    address_list = []
    br = BinaryReader(bv)
    for ea in range(start_adress, end_address, 4):
        br.offset = ea
        ea_value_Dword = br.read32()
        if ea_value_Dword < guess_file_end and (ea_value_Dword % 2) != 0 and ea_value_Dword > guess_base_address_start: 
            if (ea_value_Dword-1) not in address_list:
                address_list.append(ea_value_Dword-1)
    br.offset = 0
    print("point search over")
    return address_list

def do_calc_flag(disass_address_list,point_address_list):
    guess_address_flag = {}
    for base_addr in range(guess_base_address_start, guess_base_address_end, acc):
        flag = 0
        for i in disass_address_list:
            if (i + base_addr) in point_address_list:
                flag = flag + 1
        guess_address_flag[base_addr] = flag
    #print (str(str(flag) +" -> "+hex(base_addr) + " "))
    return guess_address_flag

def show_result(guess_address_flag):
    #print(guess_address_flag)
    xdata = list(guess_address_flag.keys())
    ydata = list(guess_address_flag.values())
    plt.plot(xdata,ydata)
    plt.ticklabel_format(useOffset=False)
    print ("The load address maybe is:"+hex(xdata[ydata.index(max(ydata))]))
    print ("Please read plt to find more infomation!") 
    plt.show()


t = time.perf_counter()
l1 = do_find_disass(bv.start,bv.end)
print(f'coast:{time.perf_counter() - t:.8f}s')

t = time.perf_counter()
l2 = do_find_point(bv.start,bv.end)
print(f'coast:{time.perf_counter() - t:.8f}s')

t = time.perf_counter()
d1 = do_calc_flag(l1,l2)
print(f'coast:{time.perf_counter() - t:.8f}s')

show_result(d1)



