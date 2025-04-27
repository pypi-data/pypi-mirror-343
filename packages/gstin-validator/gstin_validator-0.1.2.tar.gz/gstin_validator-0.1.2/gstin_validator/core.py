def validate_gstin(gstin: str) -> bool:
    check = gstin[-1]
    gst = gstin[:-1]
    csum=validate_checksum(gst)
    print(gst)
    l = [int(c) if c.isdigit() else ord(c)-55 for c in gst]
    l = [val*(ind % 2 + 1) for (ind, val) in list(enumerate(l))]
    l = [(int(x/36) + x%36) for x in l]
    csum = (36 - sum(l)%36)
    csum = str(csum) if (csum < 10) else chr(csum + 55)
    print(csum)
    return True if (check == csum) else False



def validate_checksum(gst: str) -> str:
    l = [int(c) if c.isdigit() else ord(c) - 55 for c in gst]
    l = [val * (ind % 2 + 1) for (ind, val) in list(enumerate(l))]
    l = [(int(x / 36) + x % 36) for x in l]
    csum = (36 - sum(l) % 36)
    csum = str(csum) if (csum < 10) else chr(csum + 55)
    return csum
    
    