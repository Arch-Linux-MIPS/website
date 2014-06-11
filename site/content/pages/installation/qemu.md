Title: QEMU
Status: hidden

It's pretty easy to run Arch Linux MIPS under QEMU's full system
emulation by targetting the Malta development board. The following text
will walk through setting that up.

# Root filesystem disk image

The downloadable rootfs is provided as a tarball in order to keep file
size minimal & provide maximum versatility. You'll need to generate a
disk image containing a filesystem and the content from that tarball
which we can provide to QEMU.

* Download the [latest malta root filesystem tarball](http://archlinuxmips.org/dl/archlinux-mips32r2el-malta-201406112046.tar.xz).
* Create an empty file that will be the disk image, for example to generate a 4GB image:

	$ dd if=/dev/zero of=root.bin bs=1G count=4

* Format that image with a filesystem. For example to use ext4 which matches the U-boot setup below:

	$ mkfs.ext4 root.bin

* Mount that filesystem:

	$ mkdir root_mnt
	$ mount -o loop root.bin root_mnt

* Extract the tarball into the new filesystem:

	$ tar xaf archlinux-mips32r2el-malta-*.tar.xz -C root_mnt

* Unmount the filesystem:

	$ umount root_mnt

At this point, root.bin is a filesystem image containing an Arch Linux
MIPS root filesystem. You may remove the root_mnt directory if you wish.

# Malta monitor flash

QEMU can load kernels without the assistence of a bootloader, so
strictly speaking there is no need for a monitor flash image. However in
this setup the kernel is held within a disk image, so cannot be provided
directly to QEMU. It's easy enough to extract the kernel binary from the
image and provide that to QEMU, but then you would need to remember to
re-extract the kernel each time it is updated. A more robust solution is
to use a monitor flash image containing the U-boot bootloader. QEMU runs
U-boot, then U-boot loads the kernel directly from the disk image.

## Prebuilt flash image

The easiest way to get up & running is to download [a prebuilt Malta
monitor flash image](http://archlinuxmips.org/dl/malta-flash-uboot-201406112119.bin)
which contains the U-boot bootloader. Substitute the name flash.bin in
subsequent instructions for the name of the downloaded image, and skip
the next section.

## Generating a flash image

### Build U-boot

First of all you'll need to build U-boot. Download the latest release
or clone the git repository, see [denx.de](http://www.denx.de/wiki/U-Boot/SourceCode)
for details. Then build for a little endian Malta:

	$ make distclean
	$ make maltael_config
	$ CROSS_COMPILE=/opt/mips-2013.11/bin/mips-linux-gnu- make

Change CROSS_COMPILE above to point to a MIPS cross compiler. The Mentor
Sourcery CodeBench Lite releases are free, easy & generally work well.

### Generate U-boot environment

U-boot is very configurable, so you'll need to provide it with some
environment variables in order to tell it what to do. You could set
these from within U-boot itself but you can equally well set them in
advance whilst creating the image.

* Create a file named env.txt with the environment variables in a
key=value format, one variable per line. For example:

	bootcmd=ext4load ide 0 0x88000000 /boot/vmlinux-malta.uImage; bootm 0x88000000
	bootargs=console=ttyS0,115200 root=/dev/hda rw
	bootdelay=2

* Generate an environment image:

	$ /path/to/u-boot/tools/mkenvimage -s 131072 -o env.bin env.txt

### Assemble the flash image

Now you have the raw parts, u-boot.bin & env.bin, so it's time to
assemble them into a monitor flash image.

* QEMU has a feature which reverses the endianness of the monitor flash
when running in little endian mode, which is done in order to allow for
bi-endian flash images to function. Reverse the storage endianness here
in order to cancel that out:

	$ objcopy -I binary -O binary --reverse-bytes=4 u-boot.bin flash.bin

* Append the environment at the end of the image:

	$ dd if=env.bin of=flash.bin bs=1 seek=4063232

That's it! You can now use flash.bin as a Malta monitor flash image.

# Running QEMU

Now that you have disk & monitor flash images it's time to run QEMU:

	$ qemu-system-mipsel -m 1G -pflash flash.bin -hda root.bin

Switch to the serial console (Ctrl+Alt+3) and you should see Arch Linux
booting. See the [QEMU documentation](http://wiki.qemu.org/download/qemu-doc.html#sec_005finvocation)
for information about further QEMU options such as directing the serial
console to a pty or stdio.
