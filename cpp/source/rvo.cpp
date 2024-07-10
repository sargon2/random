// When working on Shrinkers, I ran into a problem where part of the struct I
// was creating was deallocated upon exit of the creation function.

// It turns out the problem has almost nothing to do with RVO, but rather with
// the fact that I was using automatic storage duration for the strings in the
// struct. This means that the strings are deallocated when the function exits,
// and the struct is left with dangling pointers.

// RVO is just a way to optimize the copying of objects in C++. It's not
// guaranteed to happen, but it's a common optimization that compilers will
// perform, and it doesn't prevent the deallocation of return values on its own,
// it just optimizes what's already happening.

// https://en.cppreference.com/w/cpp/language/copy_elision

#include "rvo.h"
#include <iostream>

// Doesn't work because the strings are deallocated when the function exits
// testStruct *createStruct() {
//     const char *strings[] = {"Hello",
//                              "World"}; // "Automatic" storage duration --
//                              will
//                                        // be deallocated when the function
//                                        exits
//     testStruct *ts = new testStruct();
//     ts->a = 5;
//     ts->listOfStrings = strings;
//     return ts;
// }

testStruct *createStruct2() {
    const char **strings = new const char *[] {
        "Hello", "World"
    }; // "Dynamic" storage duration -- will need to be deallocated manually
    testStruct *ts = new testStruct();
    ts->a = 5;
    ts->listOfStrings = strings;
    return ts;
}

void destructStruct(testStruct *ts) {
    delete ts->listOfStrings;
    delete ts;
}

void tryStructCreation() {
    testStruct *ts = createStruct2();
    std::cout << ts->a << std::endl;
    std::cout << ts->listOfStrings[0] << std::endl;
    std::cout << ts->listOfStrings[1] << std::endl;
    auto strs = ts->listOfStrings;
    destructStruct(ts);
    // std::cout << "0" << strs[0]
    //           << std::endl; // Crashes because it's deallocated
    // std::cout << "1" << strs[1] << std::endl;
}

// Original problematic code from Shrinkers source/vulkan.cpp:

// VkInstanceCreateInfo *createCreateInfo(SDL_Window *window,
//                                        bool enableValidationLayers) {

//     // TODO: This is calling new, and leaking memory

//     // App info is optional but it may provide some useful information to the
//     // driver
//     VkApplicationInfo *appInfo = new VkApplicationInfo();
//     appInfo->sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
//     appInfo->pApplicationName = "Hello Triangle";
//     appInfo->applicationVersion = VK_MAKE_VERSION(1, 0, 0);
//     appInfo->pEngineName = "No Engine";
//     appInfo->engineVersion = VK_MAKE_VERSION(1, 0, 0);
//     appInfo->apiVersion = VK_API_VERSION_1_0;

//     VkInstanceCreateInfo *createInfo = new VkInstanceCreateInfo();
//     createInfo->sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
//     createInfo->pApplicationInfo = appInfo;

//     // Get required extensions

//     uint32_t sdlExtensionCount = 0;
//     if (!SDL_Vulkan_GetInstanceExtensions(window, &sdlExtensionCount,
//                                           nullptr)) {
//         throw std::runtime_error(
//             std::string(
//                 "Failed to get the number of required instance extensions: ")
//                 +
//             SDL_GetError());
//     }

//     std::vector<const char *> *extensions =
//         new std::vector<const char *>(sdlExtensionCount);
//     if (!SDL_Vulkan_GetInstanceExtensions(window, &sdlExtensionCount,
//                                           extensions->data())) {
//         throw std::runtime_error(
//             std::string("Failed to get the required instance extensions: ") +
//             SDL_GetError());
//     }

//     if (enableValidationLayers) {
//         extensions->push_back(VK_EXT_DEBUG_UTILS_EXTENSION_NAME);
//     }

//     createInfo->enabledExtensionCount =
//         static_cast<uint32_t>(extensions->size());
//     createInfo->ppEnabledExtensionNames = extensions->data();

//     std::vector<const char *> *validationLayers = new std::vector<const char
//     *>;

//     if (enableValidationLayers) {
//         validationLayers->push_back("VK_LAYER_KHRONOS_validation");
//         createInfo->enabledLayerCount =
//             static_cast<uint32_t>(validationLayers->size());
//         createInfo->ppEnabledLayerNames = validationLayers->data();
//     } else {
//         createInfo->enabledLayerCount = 0;
//     }

//     if (enableValidationLayers &&
//         !checkValidationLayerSupport(validationLayers)) {
//         throw std::runtime_error(
//             "validation layers requested, but not available!");
//     }

//     return createInfo;
// }
