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

// TODO see
// https://medium.com/@aliaksei.radzevich/compile-time-dependency-injection-in-c-managing-dependencies-without-late-binding-4338e0afcc44

#include <functional>
#include <iostream>
#include <typeindex>
#include <unordered_map>

template <typename T> class Singleton {
  public:
    static T &instance() {
        static T instance;
        return instance;
    };

    Singleton(const Singleton &) = delete;
    Singleton &operator=(const Singleton) = delete;

  protected:
    Singleton() {}
};

class DIRegistry : public Singleton<DIRegistry> {
  public:
    // Register a factory function that creates an object of type T
    // Usage: registerFactory(fn);
    // No need to specify template types, they are inferred from the function
    template <typename T, typename... Args>
    void registerFactory(T (*creator)(Args...)) {
        creators[typeid(T)] = [this, creator]() {
            return std::make_shared<T>(createDependency<Args>()...);
        };
    }

    // Given types as template arguments, create and register a factory.
    // Usage: createFactory<TypeToProduce, TypeOfArg1, TypeOfArg2, ...>();
    template <typename T, typename... Args> void createFactory() {
        creators[typeid(T)] = [this]() {
            return std::make_shared<T>(T(createDependency<Args>()...));
        };
    }

    template <typename T> std::shared_ptr<T> get() {
        auto it = creators.find(typeid(T));
        if (it != creators.end()) {
            // TODO keep a registry of created objects and allow creator
            // functions to specify whether the same dep should be returned each
            // time or a new one created.  We should use soft pointers to allow
            // reference-counting GC to work.
            return std::static_pointer_cast<T>(it->second());
        }
        throw std::runtime_error("Dependency not found");
    }

  private:
    std::unordered_map<std::type_index, std::function<std::shared_ptr<void>()>>
        creators;

    template <typename T> T createDependency() { return *get<T>(); }
};

class A {
  public:
    A() { std::cout << "A constructor\n"; }
};

class B {
  public:
    B(A a) { std::cout << "B constructor\n"; }
};

class C {
  public:
    C(A a, B b) { std::cout << "C constructor\n"; }
};

int try_dep_injection() {
    // TODO can we pass args like <C(A, B)> instead of <C, A, B>?
    DIRegistry::instance().createFactory<A>();
    DIRegistry::instance().createFactory<B, A>();
    DIRegistry::instance().createFactory<C, A, B>();

    DIRegistry &registry = DIRegistry::instance();

    std::shared_ptr<C> c = registry.get<C>();
    std::shared_ptr<B> b = registry.get<B>();
    std::shared_ptr<A> a = registry.get<A>();

    return 0;
}
