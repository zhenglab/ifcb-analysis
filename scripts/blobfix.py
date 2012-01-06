from sys import argv
from os import makedirs, path, uname
import re
from zipfile import ZipFile
from time import strftime, time, gmtime

QUEUE='blobfix20120106a'

INDIR='/scratch/ifcb'
BLOBDIR='/scratch/ifcb/blobs'
OUTDIR='/scratch/ifcb/good_blobs'

# the weekend ... starts here
def fix(lid):
    (day, year) = re.match(r'IFCB._((\d+)_\d+)_\d+',lid).groups()
    try:
        makedirs(path.join(OUTDIR,year,day))
    except:
        pass
    binzip = path.join(INDIR,year,day,lid+'.zip')
    badblobzip = path.join(BLOBDIR,year,day,lid+'_blobs.zip')
    goodblobzip = path.join(OUTDIR,year,day,lid+'_blobs_v2.zip')

    # now open all three files.
    try:
        bin = ZipFile(binzip,'r')
        bad = ZipFile(badblobzip,'r')
        good = ZipFile(goodblobzip,'w')
    except:
        raise

    # first entries are csv and xml records
    for name in bin.namelist()[:2]:
        good.writestr(name, bin.read(name))
    # compare bin names (right) with blob zip names (wrong)
    for (right,wrong) in zip(bin.namelist()[2:], bad.namelist()):
        bytes = bad.read(wrong) # right data, wrong name
        good.writestr(right,bytes) # now it has the right name
    # now write a receipt
    receipt = 'Blob fixed at %s on %s\n' % (strftime('%Y-%m-%dT%H:%M:%SZ',gmtime(time())), ' '.join(uname()))
    good.writestr('receipt.txt', receipt)
    
    try:
        good.close()
        bad.close()
        bin.close()
    except:
        raise

if __name__=='__main__':
    lid = argv[1]
    fix(lid)
