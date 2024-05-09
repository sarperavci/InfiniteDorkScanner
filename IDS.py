from Crypto.Cipher import AES 
from Crypto.Util.Padding import unpad
import hashlib , random, os ,time
from colorama import Fore, init
import sys 

class IDS:
    def __init__(self, output  , limit ):
        self.files =[f for f in os.listdir('data') if f.endswith('.txt')]
        self.limit =  limit
        self.urlIndexes = []
        self.output = output
        self.fileLineCount = 152000
        self.counter = 0
        
    def decrypt(self,ct,index):
        cipher = AES.new(hashlib.sha256(str(index).encode() + self.current_file.encode()).digest(), AES.MODE_ECB)
        ct_bytes = bytes.fromhex(ct)
        return unpad(cipher.decrypt(ct_bytes), AES.block_size).decode()
    
    def selectRandomFile(self):
        self.current_file = random.choice(self.files)
    
    def generateRandomIndexes(self, n):
        self.urlIndexes = random.sample(range(0,  self.fileLineCount), n)

    def readFileAndDecrypt(self):
        self.urls = []
        with open('data/'+self.current_file) as fp:
            for i, line in enumerate(fp):
                if i in self.urlIndexes:
                    pt = self.decrypt(line,i)
                    self.urls.append(pt)
            
    def start(self):
        print(Fore.GREEN + '[+] Starting IDS')
        CYCLE_COUNT = random.randint(3,7)
        t0 = time.time()
        for _ in range(CYCLE_COUNT):
            time.sleep(0.34)
            self.selectRandomFile()
            self.generateRandomIndexes(random.randint(self.limit//CYCLE_COUNT, min( int(self.limit//CYCLE_COUNT*1.5), self.fileLineCount)))
            self.readFileAndDecrypt()
            print(Fore.GREEN + f"[+] Scraped +{len(self.urls)} URLs" )
            self.counter += len(self.urls)
            temp_urls = self.urls
            with open(self.output, 'a+') as f:
                for url in temp_urls:
                    f.write(url)   
        print()
        print(Fore.YELLOW + f'[i] Scraped {self.counter} URLs in {int(time.time()-t0)} seconds')    

     
init(autoreset=True)
if __name__ == '__main__':    
    print(Fore.YELLOW + "[i] " +  "Welcome to the IDS, Infinite Dork Scanner")
    print(Fore.RED    + "[!] " +  "We are not responsible for any damage caused by the IDS")
    print(Fore.RED    + "[!] " +  "Use this tool for educational purposes only")
    print(Fore.RED    + "[!] " +  "This tool is a demo of a real IDS. This retrieves URLs from a list")
    print()
    if '--help' in sys.argv:
        print(Fore.YELLOW + "[i] " + Fore.WHITE +  "Usage: python3 IDS.py --limit <limit> --output <output>")
        print(Fore.YELLOW + "[i] " + Fore.WHITE +  "Example: python3 IDS.py --limit 100 --output output.txt")
        exit(0)

    if '--limit' in sys.argv:
        limit = int(sys.argv[sys.argv.index('--limit')+1])
    else:
        print(Fore.YELLOW + "[i] " + Fore.WHITE +  "Limit not provided, using default limit of 100")
        limit = 100
    if limit > 10000:
        print(Fore.RED + "[!] " + Fore.WHITE +  "Limit is too high, please keep it under 10000")
        exit(0)

    if '--output' in sys.argv:
        output = sys.argv[sys.argv.index('--output')+1]
    else:
        print(Fore.YELLOW + "[i] " + Fore.WHITE +  "Output file not provided, using default output file output.txt", end='\n\n')
        output = 'output.txt'

    ids = IDS(  output, limit )
    ids.start()