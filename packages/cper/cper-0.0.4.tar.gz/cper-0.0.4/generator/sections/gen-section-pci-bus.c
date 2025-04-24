/**
 * Functions for generating pseudo-random CPER PCI/PCI-X bus error sections.
 *
 * Author: Lawrence.Tang@arm.com
 **/

#include <stdlib.h>
#include <libcper/BaseTypes.h>
#include <libcper/generator/gen-utils.h>
#include <libcper/generator/sections/gen-section.h>

//Generates a single pseudo-random PCI/PCI-X bus error section, saving the resulting address to the given
//location. Returns the size of the newly created section.
size_t generate_section_pci_bus(void **location,
				GEN_VALID_BITS_TEST_TYPE validBitsType)
{
	//Create random bytes.
	int size = 72;
	UINT8 *bytes = generate_random_bytes(size);

	//Set reserved areas to zero.
	UINT64 *validation = (UINT64 *)bytes;
	*validation &= 0x1FF; //Validation 9-63
	if (validBitsType == ALL_VALID) {
		*validation = 0x1FF;
	} else if (validBitsType == SOME_VALID) {
		*validation = 0x155;
	}
	UINT32 *reserved = (UINT32 *)(bytes + 20);
	*reserved = 0;
	UINT64 *bus_command = (UINT64 *)(bytes + 40);
	*bus_command &= ((UINT64)0x1 << 56); //Bus command bytes bar bit 56.

	//Fix values that could be above range.
	UINT16 *error_type = (UINT16 *)(bytes + 16);
	*error_type = cper_rand() % 8;

	//Fix error status.
	create_valid_error_section(bytes + 8);

	//Set return values, exit.
	*location = bytes;
	return size;
}
