addr_start = 0x26000
addr_end = 0x90000
b = 0x281E5
for ea in range(addr_start,addr_end,2):
    Dword = idc.get_wide_dword(ea)
    #print hex(Dword)
    if Dword == b:
        print (hex(ea))
