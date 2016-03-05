import bisect
class FuncAddr:
	def __init__(self, begin):
		self.begin = begin
	def __lt__(self, other):
		return self.begin < other.begin
	def __le__(self, other):
		return self.begin <= other.begin
	def __gt__(self, other):
		return self.begin > other.begin
	def __ge__(self, other):
		return self.begin >= other.begin
	def __eq__(self, other):
		return other != None and self.begin == other.begin

class Func(FuncAddr):
	def __init__(self, index, begin, packed, fragment, fixup, name):
		FuncAddr.__init__(self, begin)
		self.index = index
		self.packed = packed
		self.fragment = fragment
		self.fixup = fixup
		self.name = name
	def __str__(self):
		if self.name == None:
			return "sub_" + hex(self.begin)[2:]
		return self.name

def loadnames():
	out = []
	with open("/home/zhuowei/fromraspi/kernelsyms.txt", "r") as infile:
		started = False
		for l in infile:
			if not started and l.startswith("  00000000"):
				started = True
			if not started:
				continue
			if not l.startswith("  "):
				break
			p = l.split()
			o = Func(int(p[0], 16), int(p[1], 16),
				p[2] == "Y", p[3] == "Y",
				p[4] == "Y",
				p[5] if len(p) >= 6 else None)
			out.append(o)
	return out

names = loadnames()
def find_le(a, x):
	i = bisect.bisect_right(a, x)
	if i:
		return a[i-1]
	return None
def lookupaddr(addr):
	return find_le(names, FuncAddr(addr))
