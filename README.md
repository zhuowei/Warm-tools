Warm is a collection of tools to investigate Windows on ARM. It's probably useless for you.

Licensed under Apache License, v2.

##d.py

GDB script to help debug Windows IoT for Raspberry Pi 2 running in QEMU with QEMU's gdbstub. Made because the kernel debugger wasn't working over the emulated serial, adn I don't know how to attach WinDBG directly to QEMU.

Current features:

- `findbase` to attempt to guess the load offset of the image (0x400000 + ? = virtual address) by searching for 16 bytes after $PC
- Stack unwinding using the r11 frame pointer
- Frame decorator that prints out function names given a list of symbols; must run `findbase` before use

Tested with Windows IoT 10586's Raspberry Pi 2 image and Ubuntu 15.10's `gdb-multiarch` and `qemu-system-arm` packages.

You probably want to put this in your .gdbinit:
```
set gnutarget elf32-littlearm
set architecture arm
source ~/warm/d.py
target remote :1234
set python print-stack full
```

### dumping symbols for frame decorator

Warm needs a dump of the symbols in ntoskrnl; you can get this with Visual Studio's dumpbin.

```
"C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\symchk.exe" \docs\winprogress\winiot_rp2\ntoskrnl_2.exe
dumpbin \docs\winprogress\winiot_rp2\ntoskrnl_2.exe /pdata >kernelsyms.txt
```
