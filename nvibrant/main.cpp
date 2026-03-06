#include <cstring>
#include <vector>
#include <fstream>
#include <fcntl.h>
#include <sys/ioctl.h>

// Open GPU Kernel Modules
#include "nvkms-ioctl.h"
#include "nvkms-api.h"

// ----------------------------------------------------------------------------|

// NvKms ioctl calls must match the driver version
const char* NVIDIA_DRIVER_VERSION = []() {

    // Safety fallback or override with environment variable
    if (const char* version = getenv("NVIDIA_DRIVER_VERSION_CPP"))
        return version;

    // Seems to be a common and stable path to get the information
    if (auto file = std::ifstream("/sys/module/nvidia/version")) {
        static std::string version;
        std::getline(file, version);
        return version.c_str();
    }

    printf("Could not find the current driver version from /sys/module/nvidia/version\n");
    printf("• Run with 'NVIDIA_DRIVER_VERSION_CPP=x.y.z nvibrant' to set or force it\n");
    exit(1);
}();

// Nth GPU index to allocate device handle
const NvU32 NVIDIA_GPU = []() {
    if (const char* num = getenv("NVIDIA_GPU"))
        return atoi(num);
    return 0;
}();

// What attribute to set on the displays
const char* ATTRIBUTE = []() {
    if (const char* name = getenv("ATTRIBUTE"))
        return name;
    return "vibrance";
}();

// Wrapper to populate a NvKmsIoctlParams and call ioctl for generic types
template <typename T> int easy_nvkms_ioctl(int fd, NvU32 cmd, T* data) {
    NvKmsIoctlParams params;
    params.cmd     = cmd;
    params.size    = sizeof(T);
    params.address = (NvU64) data;
    return ioctl(fd, NVKMS_IOCTL_IOWR, &params);
}

// Smart parse, limit, safe default an integer from argv at a given index
int get_int(int argc, char* argv[], int index, int min, int max, int fallback) {
    return std::max(min, std::min(max, (index < argc) ? atoi(argv[index]) : fallback));
}

// ----------------------------------------------------------------------------|

int main(int argc, char *argv[]) {
    printf("Driver version: (%s)\n", NVIDIA_DRIVER_VERSION);

    // Open the nvidia-modeset file descriptor
    int modeset = open("/dev/nvidia-modeset", O_RDWR);
    if (modeset < 0) {
        printf("Failed to open /dev/nvidia-modeset device file for ioctl calls\n");
        printf("• Perhaps 'nvidia_drm.modeset=1' kernel parameter is missing?\n");
        return 1;
    }

    // Initialize nvkms to get a deviceHandle, dispHandle, etc.
    struct NvKmsAllocDeviceParams allocDevice;
    memset(&allocDevice, 0, sizeof(allocDevice));
    memcpy(&allocDevice.request.deviceId, &NVIDIA_GPU, sizeof(NvU32));
    strcpy(allocDevice.request.versionString, NVIDIA_DRIVER_VERSION);
    allocDevice.request.no3d = NV_TRUE;
    if (easy_nvkms_ioctl(modeset, NVKMS_IOCTL_ALLOC_DEVICE, &allocDevice) < 0) {
        switch (allocDevice.reply.status) {
            case NVKMS_ALLOC_DEVICE_STATUS_VERSION_MISMATCH:
                printf("Driver version mismatch, maybe reboot?\n");
                return 1;
            default:
                printf("AllocDevice ioctl failed\n");
                return 1;
        }
    }

    // Current Nth target monitor
    int index = 0;

    // Iterate on all displays in the system, querying their info
    for (NvU32 display=0; display<allocDevice.reply.numDisps; display++) {
        printf("\nDisplay %d:\n", display);
        NvKmsQueryDispParams queryDisp;
        queryDisp.request.deviceHandle = allocDevice.reply.deviceHandle;
        queryDisp.request.dispHandle   = allocDevice.reply.dispHandles[display];
        if (easy_nvkms_ioctl(modeset, NVKMS_IOCTL_QUERY_DISP, &queryDisp) < 0) {
            printf(" QueryDisp ioctl failed\n");
            continue;
        }

        // Iterate on all physical connections of the GPU (literally, hdmi, dp, etc.)
        for (NvU32 connector=0; connector<queryDisp.reply.numConnectors; connector++) {
            index++;

            // Get 'immutable' static data (such as connector type)
            NvKmsQueryConnectorStaticDataParams staticData;
            staticData.request.deviceHandle    = allocDevice.reply.deviceHandle;
            staticData.request.dispHandle      = allocDevice.reply.dispHandles[display];
            staticData.request.connectorHandle = queryDisp.reply.connectorHandles[connector];
            if (easy_nvkms_ioctl(modeset, NVKMS_IOCTL_QUERY_CONNECTOR_STATIC_DATA, &staticData) < 0) {
                printf("QueryConnector ioctl failed\n");
                continue;
            }

            // Get the 'dynamic' data (is connected?)
            NvKmsQueryDpyDynamicDataParams dynamicData;
            dynamicData.request.deviceHandle    = allocDevice.reply.deviceHandle;
            dynamicData.request.dispHandle      = allocDevice.reply.dispHandles[display];
            dynamicData.request.dpyId           = staticData.reply.dpyId;
            if (easy_nvkms_ioctl(modeset, NVKMS_IOCTL_QUERY_DPY_DYNAMIC_DATA, &dynamicData) < 0) {
                printf("QueryDpy ioctl failed\n");
                continue;
            }

            // Print basic display info
            printf("• (%d, ", connector);
            switch (staticData.reply.type) {
                case NVKMS_CONNECTOR_TYPE_DP:    printf("DP  "); break;
                case NVKMS_CONNECTOR_TYPE_VGA:   printf("VGA "); break;
                case NVKMS_CONNECTOR_TYPE_DVI_I: printf("DVII"); break;
                case NVKMS_CONNECTOR_TYPE_DVI_D: printf("DVID"); break;
                case NVKMS_CONNECTOR_TYPE_ADC:   printf("ADC "); break;
                case NVKMS_CONNECTOR_TYPE_LVDS:  printf("LVDS"); break;
                case NVKMS_CONNECTOR_TYPE_HDMI:  printf("HDMI"); break;
                case NVKMS_CONNECTOR_TYPE_USBC:  printf("USBC"); break;
                case NVKMS_CONNECTOR_TYPE_DSI:   printf("DSI "); break;
                default: break;
            }
            printf(") • ");

            // Make the request to set attribute for this monitor
            NvKmsSetDpyAttributeParams setDpyAttr;
            setDpyAttr.request.deviceHandle = allocDevice.reply.deviceHandle;
            setDpyAttr.request.dispHandle   = allocDevice.reply.dispHandles[display];
            setDpyAttr.request.dpyId        = staticData.reply.dpyId;

            // Branch on what display attribute to set
            if (strcmp(ATTRIBUTE, "vibrance") == 0) {
                setDpyAttr.request.attribute = NV_KMS_DPY_ATTRIBUTE_DIGITAL_VIBRANCE;
                setDpyAttr.request.value     = get_int(argc, argv, index, -1024, 1023, 0);
            } else if (strcmp(ATTRIBUTE, "dithering") == 0) {
                setDpyAttr.request.attribute = NV_KMS_DPY_ATTRIBUTE_REQUESTED_DITHERING;
                setDpyAttr.request.value     = get_int(argc, argv, index, 0, 2, 2);
            } else {
                printf("Unknown attribute '%s' to set\n", ATTRIBUTE);
                continue;
            }
            printf("Set %s (%5lld) • ", ATTRIBUTE, setDpyAttr.request.value);

            // Can't set attributes on disconnected outputs
            if (!dynamicData.reply.connected) {
                printf("None\n");
                continue;
            }

            if (easy_nvkms_ioctl(modeset, NVKMS_IOCTL_SET_DPY_ATTRIBUTE, &setDpyAttr) < 0) {
                printf("Failed\n");
                continue;
            }
            printf("Success\n");
        }
    }

    // Deallocate device just in case it's not gc-ed on the driver side
    struct NvKmsFreeDeviceParams freeDevice;
    freeDevice.request.deviceHandle = allocDevice.reply.deviceHandle;
    if (easy_nvkms_ioctl(modeset, NVKMS_IOCTL_FREE_DEVICE, &freeDevice) < 0) {
        printf("Failed to free device handle\n");
        return 1;
    }

    return 0;
}