/**
 * Defines tests for validating CPER-JSON IR output from the cper-parse library.
 *
 * Author: Lawrence.Tang@arm.com
 **/

#include "test-utils.h"
#include "string.h"
#include "assert.h"
#include <ctype.h>
#include <json.h>
#include <libcper/cper-parse.h>
#include <libcper/generator/cper-generate.h>
#include <libcper/generator/sections/gen-section.h>
#include <libcper/json-schema.h>
#include <libcper/sections/cper-section.h>

#include "base64_test.h"

/*
* Test templates.
*/
static const GEN_VALID_BITS_TEST_TYPE allValidbitsSet = ALL_VALID;
static const GEN_VALID_BITS_TEST_TYPE fixedValidbitsSet = SOME_VALID;
static const int GEN_EXAMPLES = 0;

static const char *cper_ext = "cperhex";
static const char *json_ext = "json";

struct file_info {
	char *cper_out;
	char *json_out;
};

void free_file_info(struct file_info *info)
{
	if (info == NULL) {
		return;
	}
	free(info->cper_out);
	free(info->json_out);
	free(info);
}

struct file_info *file_info_init(const char *section_name)
{
	struct file_info *info = NULL;
	char *buf = NULL;
	size_t size;
	int ret;

	info = (struct file_info *)calloc(1, sizeof(struct file_info));
	if (info == NULL) {
		goto fail;
	}

	size = strlen(LIBCPER_EXAMPLES) + 1 + strlen(section_name) + 1 +
	       strlen(cper_ext) + 1;
	info->cper_out = (char *)malloc(size);
	ret = snprintf(info->cper_out, size, "%s/%s.%s", LIBCPER_EXAMPLES,
		       section_name, cper_ext);
	if (ret != (int)size - 1) {
		printf("snprintf0 failed\n");
		goto fail;
	}
	size = strlen(LIBCPER_EXAMPLES) + 1 + strlen(section_name) + 1 +
	       strlen(json_ext) + 1;
	info->json_out = (char *)malloc(size);
	ret = snprintf(info->json_out, size, "%s/%s.%s", LIBCPER_EXAMPLES,
		       section_name, json_ext);
	if (ret != (int)size - 1) {
		printf("snprintf3 failed\n");
		goto fail;
	}
	free(buf);
	return info;

fail:
	free(buf);
	free_file_info(info);
	return NULL;
}

void cper_create_examples(const char *section_name)
{
	//Generate full CPER record for the given type.
	json_object *ir = NULL;
	size_t size;
	size_t file_size;
	FILE *outFile = NULL;
	unsigned char *file_data;
	FILE *record = NULL;
	char *buf = NULL;
	struct file_info *info = file_info_init(section_name);
	if (info == NULL) {
		goto done;
	}

	record = generate_record_memstream(&section_name, 1, &buf, &size, 0,
					   fixedValidbitsSet);

	// Write example CPER to disk
	outFile = fopen(info->cper_out, "wb");
	if (outFile == NULL) {
		printf("Failed to create/open CPER output file: %s\n",
		       info->cper_out);
		goto done;
	}

	fseek(record, 0, SEEK_END);
	file_size = ftell(record);
	rewind(record);
	file_data = malloc(file_size);
	if (fread(file_data, 1, file_size, record) != file_size) {
		printf("Failed to read CPER data from memstream.");
		fclose(outFile);
		assert(0);

		goto done;
	}
	for (size_t index = 0; index < file_size; index++) {
		char hex_str[3];
		int out = snprintf(hex_str, sizeof(hex_str), "%02x",
				   file_data[index]);
		if (out != 2) {
			printf("snprintf1 failed\n");
			goto done;
		}
		fwrite(hex_str, sizeof(char), 2, outFile);
		if (index % 30 == 29) {
			fwrite("\n", sizeof(char), 1, outFile);
		}
	}
	fclose(outFile);

	//Convert to IR, free resources.
	rewind(record);
	ir = cper_to_ir(record);
	if (ir == NULL) {
		printf("Empty JSON from CPER bin2\n");
		assert(0);
		goto done;
	}

	//Write json output to disk
	json_object_to_file_ext(info->json_out, ir, JSON_C_TO_STRING_PRETTY);
	json_object_put(ir);

done:
	free_file_info(info);
	if (record != NULL) {
		fclose(record);
	}
	if (outFile != NULL) {
		fclose(outFile);
	}
	free(buf);
}

int hex2int(char ch)
{
	if ((ch >= '0') && (ch <= '9')) {
		return ch - '0';
	}
	if ((ch >= 'A') && (ch <= 'F')) {
		return ch - 'A' + 10;
	}
	if ((ch >= 'a') && (ch <= 'f')) {
		return ch - 'a' + 10;
	}
	return -1;
}

int string_to_binary(const char *source, size_t length, unsigned char **retval)
{
	size_t retval_size = length * 2;
	*retval = malloc(retval_size);
	int uppernibble = 1;

	size_t ret_index = 0;

	for (size_t i = 0; i < length; i++) {
		char c = source[i];
		if (c == '\n') {
			continue;
		}
		int val = hex2int(c);
		if (val < 0) {
			printf("Invalid hex character in test file: %c\n", c);
			return -1;
		}

		if (uppernibble) {
			(*retval)[ret_index] = (unsigned char)(val << 4);
		} else {
			(*retval)[ret_index] += (unsigned char)val;
			ret_index++;
		}
		uppernibble = !uppernibble;
	}
	return ret_index;
}

//Tests fixed CPER sections for IR validity with an example set.
void cper_example_section_ir_test(const char *section_name)
{
	//Open CPER record for the given type.
	struct file_info *info = file_info_init(section_name);
	if (info == NULL) {
		return;
	}

	FILE *cper_file = fopen(info->cper_out, "rb");
	if (cper_file == NULL) {
		printf("Failed to open CPER file: %s\n", info->cper_out);
		free_file_info(info);
		assert(0);
		return;
	}
	fseek(cper_file, 0, SEEK_END);
	size_t length = ftell(cper_file);
	fseek(cper_file, 0, SEEK_SET);
	char *buffer = (char *)malloc(length);
	if (!buffer) {
		free_file_info(info);
		return;
	}
	if (fread(buffer, 1, length, cper_file) != length) {
		printf("Failed to read CPER file: %s\n", info->cper_out);
		free(buffer);
		free_file_info(info);
		return;
	}
	fclose(cper_file);

	unsigned char *cper_bin;
	int cper_bin_len = string_to_binary(buffer, length, &cper_bin);
	if (cper_bin_len <= 0) {
		free(buffer);
		free_file_info(info);
		assert(0);
		return;
	}
	printf("cper_bin: %s\n", cper_bin);
	printf("cper_bin_len: %d\n", cper_bin_len);

	//Convert to IR, free resources.
	json_object *ir = cper_buf_to_ir(cper_bin, cper_bin_len);
	if (ir == NULL) {
		printf("Empty JSON from CPER bin3\n");
		free(cper_bin);
		free(buffer);
		free_file_info(info);
		assert(0);
		return;
	}

	json_object *expected = json_object_from_file(info->json_out);
	assert(expected != NULL);
	if (expected == NULL) {
		free(buffer);
		free(cper_bin);
		free_file_info(info);
		const char *str = json_object_to_json_string(ir);

		const char *expected_str = json_object_to_json_string(expected);
		assert(strcmp(str, expected_str) == 0);
		return;
	}

	assert(json_object_equal(ir, expected));
	free(buffer);
	free(cper_bin);
	json_object_put(ir);
	json_object_put(expected);
	free_file_info(info);
}

//Tests a single randomly generated CPER section of the given type to ensure CPER-JSON IR validity.
void cper_log_section_ir_test(const char *section_name, int single_section,
			      GEN_VALID_BITS_TEST_TYPE validBitsType)
{
	//Generate full CPER record for the given type.
	char *buf;
	size_t size;
	FILE *record = generate_record_memstream(&section_name, 1, &buf, &size,
						 single_section, validBitsType);

	//Convert to IR, free resources.
	json_object *ir;
	if (single_section) {
		ir = cper_single_section_to_ir(record);
	} else {
		ir = cper_to_ir(record);
	}

	fclose(record);
	free(buf);

	//Validate against schema.
	int valid = schema_validate_from_file(ir, single_section,
					      /*all_valid_bits*/ 1);
	json_object_put(ir);

	if (valid < 0) {
		printf("IR validation test failed (single section mode = %d)\n",
		       single_section);
		assert(0);
	}
}

int to_hex(const unsigned char *input, size_t size, char **out)
{
	*out = (char *)malloc(size * 2);
	if (out == NULL) {
		return -1;
	}
	int out_index = 0;
	for (size_t i = 0; i < size; i++) {
		unsigned char c = input[i];
		char hex_str[3];
		int n = snprintf(hex_str, sizeof(hex_str), "%02x", c);
		if (n != 2) {
			printf("snprintf2 failed with code %d\n", n);
			return -1;
		}
		(*out)[out_index] = hex_str[0];
		out_index++;
		(*out)[out_index] = hex_str[1];
		out_index++;
	}
	return out_index;
}

//Checks for binary round-trip equality for a given randomly generated CPER record.
void cper_log_section_binary_test(const char *section_name, int single_section,
				  GEN_VALID_BITS_TEST_TYPE validBitsType)
{
	//Generate CPER record for the given type.
	char *buf;
	size_t size;
	FILE *record = generate_record_memstream(&section_name, 1, &buf, &size,
						 single_section, validBitsType);
	if (record == NULL) {
		printf("Could not generate memstream for binary test");
		return;
	}

	//Convert to IR.
	json_object *ir;
	if (single_section) {
		ir = cper_single_section_to_ir(record);
	} else {
		ir = cper_to_ir(record);
	}

	//Now convert back to binary, and get a stream out.
	char *cper_buf;
	size_t cper_buf_size;
	FILE *stream = open_memstream(&cper_buf, &cper_buf_size);
	if (single_section) {
		ir_single_section_to_cper(ir, stream);
	} else {
		ir_to_cper(ir, stream);
	}
	fclose(stream);

	printf("size: %zu, cper_buf_size: %zu\n", size, cper_buf_size);

	char *buf_hex;
	int buf_hex_len = to_hex((unsigned char *)buf, size, &buf_hex);
	char *cper_buf_hex;
	int cper_buf_hex_len =
		to_hex((unsigned char *)cper_buf, cper_buf_size, &cper_buf_hex);

	assert(buf_hex_len == cper_buf_hex_len);
	assert(memcmp(buf_hex, cper_buf_hex, buf_hex_len) == 0);

	free(buf_hex);
	free(cper_buf_hex);

	//Free everything up.
	fclose(record);
	free(buf);
	free(cper_buf);
	json_object_put(ir);
}

//Tests randomly generated CPER sections for IR validity of a given type, in both single section mode and full CPER log mode.
void cper_log_section_dual_ir_test(const char *section_name)
{
	cper_log_section_ir_test(section_name, 0, allValidbitsSet);
	cper_log_section_ir_test(section_name, 1, allValidbitsSet);
	//Validate against examples
	cper_example_section_ir_test(section_name);
}

//Tests randomly generated CPER sections for binary compatibility of a given type, in both single section mode and full CPER log mode.
void cper_log_section_dual_binary_test(const char *section_name)
{
	cper_log_section_binary_test(section_name, 0, allValidbitsSet);
	cper_log_section_binary_test(section_name, 1, allValidbitsSet);
}

/*
* Non-single section assertions.
*/
void CompileTimeAssertions_TwoWayConversion()
{
	for (size_t i = 0; i < section_definitions_len; i++) {
		//If a conversion one way exists, a conversion the other way must exist.
		if (section_definitions[i].ToCPER != NULL) {
			assert(section_definitions[i].ToIR != NULL);
		}
		if (section_definitions[i].ToIR != NULL) {
			assert(section_definitions[i].ToCPER != NULL);
		}
	}
}

void CompileTimeAssertions_ShortcodeNoSpaces()
{
	for (size_t i = 0; i < generator_definitions_len; i++) {
		for (int j = 0;
		     generator_definitions[i].ShortName[j + 1] != '\0'; j++) {
			assert(isspace(generator_definitions[i].ShortName[j]) ==
			       0);
		}
	}
}

/*
* Single section tests.
*/

//Generic processor tests.
void GenericProcessorTests_IRValid()
{
	cper_log_section_dual_ir_test("generic");
}
void GenericProcessorTests_BinaryEqual()
{
	cper_log_section_dual_binary_test("generic");
}

//IA32/x64 tests.
void IA32x64Tests_IRValid()
{
	cper_log_section_dual_ir_test("ia32x64");
}
void IA32x64Tests_BinaryEqual()
{
	cper_log_section_dual_binary_test("ia32x64");
}

// void IPFTests_IRValid() {
//     cper_log_section_dual_ir_test("ipf");
// }

//ARM tests.
void ArmTests_IRValid()
{
	cper_log_section_dual_ir_test("arm");
}
void ArmTests_BinaryEqual()
{
	cper_log_section_dual_binary_test("arm");
}

//Memory tests.
void MemoryTests_IRValid()
{
	cper_log_section_dual_ir_test("memory");
}
void MemoryTests_BinaryEqual()
{
	cper_log_section_dual_binary_test("memory");
}

//Memory 2 tests.
void Memory2Tests_IRValid()
{
	cper_log_section_dual_ir_test("memory2");
}
void Memory2Tests_BinaryEqual()
{
	cper_log_section_dual_binary_test("memory2");
}

//PCIe tests.
void PCIeTests_IRValid()
{
	cper_log_section_dual_ir_test("pcie");
}
void PCIeTests_BinaryEqual()
{
	cper_log_section_dual_binary_test("pcie");
}

//Firmware tests.
void FirmwareTests_IRValid()
{
	cper_log_section_dual_ir_test("firmware");
}
void FirmwareTests_BinaryEqual()
{
	cper_log_section_dual_binary_test("firmware");
}

//PCI Bus tests.
void PCIBusTests_IRValid()
{
	cper_log_section_dual_ir_test("pcibus");
}
void PCIBusTests_BinaryEqual()
{
	cper_log_section_dual_binary_test("pcibus");
}

//PCI Device tests.
void PCIDevTests_IRValid()
{
	cper_log_section_dual_ir_test("pcidev");
}
void PCIDevTests_BinaryEqual()
{
	cper_log_section_dual_binary_test("pcidev");
}

//Generic DMAr tests.
void DMArGenericTests_IRValid()
{
	cper_log_section_dual_ir_test("dmargeneric");
}
void DMArGenericTests_BinaryEqual()
{
	cper_log_section_dual_binary_test("dmargeneric");
}

//VT-d DMAr tests.
void DMArVtdTests_IRValid()
{
	cper_log_section_dual_ir_test("dmarvtd");
}
void DMArVtdTests_BinaryEqual()
{
	cper_log_section_dual_binary_test("dmarvtd");
}

//IOMMU DMAr tests.
void DMArIOMMUTests_IRValid()
{
	cper_log_section_dual_ir_test("dmariommu");
}
void DMArIOMMUTests_BinaryEqual()
{
	cper_log_section_dual_binary_test("dmariommu");
}

//CCIX PER tests.
void CCIXPERTests_IRValid()
{
	cper_log_section_dual_ir_test("ccixper");
}
void CCIXPERTests_BinaryEqual()
{
	cper_log_section_dual_binary_test("ccixper");
}

//CXL Protocol tests.
void CXLProtocolTests_IRValid()
{
	cper_log_section_dual_ir_test("cxlprotocol");
}
void CXLProtocolTests_BinaryEqual()
{
	cper_log_section_dual_binary_test("cxlprotocol");
}

//CXL Component tests.
void CXLComponentTests_IRValid()
{
	cper_log_section_dual_ir_test("cxlcomponent-media");
}
void CXLComponentTests_BinaryEqual()
{
	cper_log_section_dual_binary_test("cxlcomponent-media");
}

//NVIDIA section tests.
void NVIDIASectionTests_IRValid()
{
	cper_log_section_dual_ir_test("nvidia");
}
void NVIDIASectionTests_BinaryEqual()
{
	cper_log_section_dual_binary_test("nvidia");
}

//Unknown section tests.
void UnknownSectionTests_IRValid()
{
	cper_log_section_dual_ir_test("unknown");
}
void UnknownSectionTests_BinaryEqual()
{
	cper_log_section_dual_binary_test("unknown");
}

//Entrypoint for the testing program.
int main()
{
	if (GEN_EXAMPLES) {
		cper_create_examples("arm");
		cper_create_examples("ia32x64");
		cper_create_examples("memory");
		cper_create_examples("memory2");
		cper_create_examples("pcie");
		cper_create_examples("firmware");
		cper_create_examples("pcibus");
		cper_create_examples("pcidev");
		cper_create_examples("dmargeneric");
		cper_create_examples("dmarvtd");
		cper_create_examples("dmariommu");
		cper_create_examples("ccixper");
		cper_create_examples("cxlprotocol");
		cper_create_examples("cxlcomponent-media");
		cper_create_examples("nvidia");
		cper_create_examples("unknown");
	}
	test_base64_encode_good();
	test_base64_decode_good();
	GenericProcessorTests_IRValid();
	GenericProcessorTests_BinaryEqual();
	IA32x64Tests_IRValid();
	IA32x64Tests_BinaryEqual();
	ArmTests_IRValid();
	ArmTests_BinaryEqual();
	MemoryTests_IRValid();
	MemoryTests_BinaryEqual();
	Memory2Tests_IRValid();
	Memory2Tests_BinaryEqual();
	PCIeTests_IRValid();
	PCIeTests_BinaryEqual();
	FirmwareTests_IRValid();
	FirmwareTests_BinaryEqual();
	PCIBusTests_IRValid();
	PCIBusTests_BinaryEqual();
	PCIDevTests_IRValid();
	PCIDevTests_BinaryEqual();
	DMArGenericTests_IRValid();
	DMArGenericTests_BinaryEqual();
	DMArVtdTests_IRValid();
	DMArVtdTests_BinaryEqual();
	DMArIOMMUTests_IRValid();
	DMArIOMMUTests_BinaryEqual();
	CCIXPERTests_IRValid();
	CCIXPERTests_BinaryEqual();
	CXLProtocolTests_IRValid();
	CXLProtocolTests_BinaryEqual();
	CXLComponentTests_IRValid();
	CXLComponentTests_BinaryEqual();
	NVIDIASectionTests_IRValid();
	NVIDIASectionTests_BinaryEqual();
	UnknownSectionTests_IRValid();
	UnknownSectionTests_BinaryEqual();
	CompileTimeAssertions_TwoWayConversion();
	CompileTimeAssertions_ShortcodeNoSpaces();

	printf("\n\nTest completed successfully.\n");

	return 0;
}
