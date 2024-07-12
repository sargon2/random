// Creating my own style of dependency injection for use with Vulkan...
// Goals:
// - Think about where & how to specify construction constants (i.e. createInfo)
// - Handle traversing the dependency graph to automatically determine order of
//     construction
// - Handle multiple different dependencies of the same type
// - Do as much as is practicable at compile time vs. runtime

// Example: config file dependency provider that provides configuration keys in
// multiple types, all from the same config file

// How do we identify a dependency?
// - By type
// - Have a string name
// - Have an enum name
// - How about if there's only one variable of that type, it's fine to forego a
// name, but as soon as there's 2 then both need a name?

// Factory methods could choose to either return the same object each time
// ("caching" factory method) or construct a new one for each dependency that
// needs it

// Config file keys would be strings.  We could look them up in the enum, I
// guess...

// Example: .h file dependency provider that has a bunch of hard-coded values in
// it, similar to a config file but parsed at compile time

// How do we discover factory methods/providers?
// - Hardcode a list of them

#include "try_dep_injection.h"
#include <iostream>
#include <map>
#include <memory>
#include <stdexcept>
#include <typeindex>

class IProvider {
  public:
    virtual ~IProvider() = default;
};

template <typename T> class Provider : public IProvider {
  public:
    virtual T *get() = 0;
};

// TODO make singleton
class ProviderRegistry {
  public:
    template <typename T>
    void registerProvider(std::shared_ptr<Provider<T>> provider) {
        providers[typeid(T)] = std::static_pointer_cast<IProvider>(provider);
    }

    template <typename T> T *getProvider() {
        auto it = providers.find(typeid(T));
        if (it == providers.end()) {
            throw std::runtime_error(
                "Provider not found for the requested type");
        }
        return static_cast<Provider<T> *>(it->second.get())->get();
    }

  private:
    std::map<std::type_index, std::shared_ptr<IProvider>> providers;
};

class int_provider : public Provider<int> {
  public:
    int_provider() { std::cout << "int_provider constructor" << std::endl; }
    int *get() {
        static int value = 3;
        return &value;
    }
};

class int_consumer {
  public:
    int_consumer(int *a) {
        std::cout << "int_consumer constructor: " << a << std::endl;
        this->a = *a;
    }

    void echo() { std::cout << "a: " << a << std::endl; }

  private:
    int a;
};

int try_dep_injection() {
    ProviderRegistry registry;
    registry.registerProvider<int>(std::make_shared<int_provider>());
    int *a = registry.getProvider<int>();

    int_consumer *c = new int_consumer(a);

    c->echo();
    return 0;
}