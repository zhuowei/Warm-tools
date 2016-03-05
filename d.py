from gdb import *
from gdb.unwinder import *
from gdb.FrameDecorator import FrameDecorator
import sys
sys.path.append("/home/zhuowei/warm")
import funcnames
class FindBaseCommand(Command):
	def __init__(self):
		Command.__init__(self, "findbase", COMMAND_DATA)
		with open("/home/zhuowei/fromraspi/ntoskrnl.exe", "rb") as infile:
			self.origexec = infile.read()
		self.slide = 0
	def invoke(self, argument, from_tty):
		pc = newest_frame().pc()
		inferior = selected_inferior()
		dat = bytes(inferior.read_memory(pc, 0x10))
		index = self.origexec.find(dat)
		obase = 0x400000
		self.slide = pc - (obase + index)
		print("pc=" + hex(pc) + " index=" + hex(index) + " obase=" +
			hex(obase) + " slide=" + hex(self.slide))

class FrameId:
	def __init__(self, sp, pc):
		self.sp = sp
		self.pc = pc

class WindowsARMUnwinder(Unwinder):
	def __init__(self):
		super(WindowsARMUnwinder, self).__init__("WindowsARM")
	def __call__(self, pending_frame):
		sp = pending_frame.read_register(13)
		pc = pending_frame.read_register(15)
		unwind_info = pending_frame.create_unwind_info(FrameId(sp, pc))
		fp = pending_frame.read_register(11)
		if int(sp) == 0:
			return unwind_info
		prevframe = selected_inferior().read_memory(fp, 8).cast("I")
		mytype = lookup_type("long")
		unwind_info.add_saved_register(13, Value(prevframe[0]).cast(mytype))
		unwind_info.add_saved_register(11, Value(prevframe[0]).cast(mytype))
		unwind_info.add_saved_register(15, Value(prevframe[1]).cast(mytype))
		return unwind_info

class WindowsARMFrameDecorator(FrameDecorator):
	def __init__(self, fobj):
		super(WindowsARMFrameDecorator, self).__init__(fobj)
	def function(self):
		if findbase.slide == 0:
			raise Exception("Hey you need to run findbase")
		pc = int(self.inferior_frame().pc())
		fun = funcnames.lookupaddr(pc - findbase.slide)
		if fun != None:
			return str(fun)
		return super(WindowsARMFrameDecorator, self).function()

class WindowsARMFrameFilter:
	def __init__(self):
		self.name = "WindowsARMFrameFilter"
		self.priority = 100
		self.enabled = True
	def filter(self, frame_iter):
		frame_iter = map(WindowsARMFrameDecorator, frame_iter)
		return frame_iter

findbase = FindBaseCommand()

unwinder = WindowsARMUnwinder()

register_unwinder(None, unwinder, True)

frame_filter = WindowsARMFrameFilter()
frame_filters[frame_filter.name] = frame_filter

print("Python script for debugging Windows on ARM in QEMU: loaded")
