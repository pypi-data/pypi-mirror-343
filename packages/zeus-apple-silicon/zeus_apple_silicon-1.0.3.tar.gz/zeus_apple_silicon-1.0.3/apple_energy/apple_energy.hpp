#pragma once

#include <iostream>
#include <optional>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

#include <CoreFoundation/CoreFoundation.h>

/* An alias for the subscription reference (forward declared). */
typedef struct __IOReportSubscriptionRef* IOReportSubscriptionRef;

extern "C" {
/* Returns a dictionary containing channels for the given group. */
CFDictionaryRef IOReportCopyChannelsInGroup(CFStringRef group,
    CFStringRef subgroup, uint64_t a,
    uint64_t b, uint64_t c);

/* Creates an IOReport subscription based on a mutable channels dictionary. */
IOReportSubscriptionRef IOReportCreateSubscription(
    const void* unused1, CFMutableDictionaryRef channels_dict,
    CFMutableDictionaryRef* unused2, uint64_t unused3, CFTypeRef unused4);

/* Creates a sample (snapshot) from the subscription. */
CFDictionaryRef IOReportCreateSamples(IOReportSubscriptionRef subs,
    CFMutableDictionaryRef channels_dict_mut,
    const void* unused);

/* Creates a “delta” sample from two snapshots. */
CFDictionaryRef IOReportCreateSamplesDelta(CFDictionaryRef sample1,
    CFDictionaryRef sample2,
    const void* unused);

/* Returns a simple integer value from the channel’s dictionary. */
int64_t IOReportSimpleGetIntegerValue(CFDictionaryRef item, int unused);

/* Returns a CFString representing the channel’s name. */
CFStringRef IOReportChannelGetChannelName(CFDictionaryRef item);

/* Returns the units of a channel. */
CFStringRef IOReportChannelGetUnitLabel(CFDictionaryRef item);
}

/*
Represents a single parsed measurement reported by `AppleEnergyMonitor`.

If a field could not be observed/detected on the current device,
it will be left as an empty `std::optional` object.

Units are in mJ.
*/
struct AppleEnergyMetrics {
    // CPU related metrics
    std::optional<int64_t> cpu_total_mj;
    std::optional<std::vector<int64_t>> efficiency_cores_mj;
    std::optional<std::vector<int64_t>> performance_cores_mj;
    std::optional<int64_t> efficiency_core_manager_mj;
    std::optional<int64_t> performance_core_manager_mj;

    // DRAM
    std::optional<int64_t> dram_mj;

    // GPU related metrics
    std::optional<int64_t> gpu_mj;
    std::optional<int64_t> gpu_sram_mj;

    // ANE
    std::optional<int64_t> ane_mj;
};

class AppleEnergyMonitor {
public:
    AppleEnergyMonitor() { initialize(); }

    ~AppleEnergyMonitor()
    {
        CFRelease(subscription);
        CFRelease(channels_dict_mutable);

        for (auto it = begin_samples.begin(); it != begin_samples.end(); ++it) {
            CFRelease(it->second);
        }
    }

    void begin_window(const std::string& key)
    {
        if (begin_samples.find(key) != begin_samples.end()) {
            throw std::runtime_error(
                "Measurement with specified key already exists.");
        }
        begin_samples[key] = IOReportCreateSamples(subscription, channels_dict_mutable, nullptr);
    }

    AppleEnergyMetrics end_window(const std::string& key)
    {
        auto it = begin_samples.find(key);
        if (it == begin_samples.end()) {
            throw std::runtime_error(
                "No measurement with provided key had been started.");
        }

        CFDictionaryRef sample1 = it->second;
        CFDictionaryRef sample2 = IOReportCreateSamples(subscription, channels_dict_mutable, nullptr);

        // Create a delta sample (the difference between the two cumulative
        // snapshots).
        CFDictionaryRef sample_delta = IOReportCreateSamplesDelta(sample1, sample2, nullptr);
        CFRelease(sample1);
        CFRelease(sample2);
        begin_samples.erase(key);

        // A delta sample is treated the same as a cumulative sample.
        AppleEnergyMetrics result = parse_sample(sample_delta);
        CFRelease(sample_delta);

        return result;
    }

    AppleEnergyMetrics get_cumulative_energy()
    {
        CFDictionaryRef sample = IOReportCreateSamples(subscription, channels_dict_mutable, nullptr);
        AppleEnergyMetrics result = parse_sample(sample);
        CFRelease(sample);
        return result;
    }

private:
    std::unordered_map<std::string, CFDictionaryRef> begin_samples;

    IOReportSubscriptionRef subscription;
    CFMutableDictionaryRef channels_dict_mutable;

    void initialize()
    {
        const char* group_cstr = "Energy Model";
        CFStringRef group_name = CFStringCreateWithCString(nullptr, group_cstr, kCFStringEncodingUTF8);
        CFDictionaryRef channels_dict = IOReportCopyChannelsInGroup(group_name, nullptr, 0, 0, 0);

        // Release string to avoid memory leak.
        CFRelease(group_name);

        // Make a mutable copy of the channels dictionary (needed for
        // subscriptions).
        CFIndex num_items = CFDictionaryGetCount(channels_dict);

        channels_dict_mutable = CFDictionaryCreateMutableCopy(nullptr, num_items, channels_dict);
        CFRelease(channels_dict);

        // Create the IOReport subscription.
        CFMutableDictionaryRef updatedChannels = nullptr;
        subscription = IOReportCreateSubscription(nullptr, channels_dict_mutable,
            &updatedChannels, 0, nullptr);

        if (subscription == nullptr) {
            throw std::runtime_error("Failed to create IOReport subscription.");
        }
    }

    AppleEnergyMetrics parse_sample(CFDictionaryRef sample)
    {
        AppleEnergyMetrics result;

        // The sample is expected to contain the channels under the key
        // "IOReportChannels".
        CFStringRef key_str = CFStringCreateWithCString(nullptr, "IOReportChannels",
            kCFStringEncodingUTF8);
        const void* channels_value = CFDictionaryGetValue(sample, key_str);
        CFRelease(key_str);

        // If parsing the sample was not possible, return a result having all fields
        // set to an empty `std::optional`, indicating that all fields are
        // unobservable.
        if (channels_value == nullptr) {
            return result;
        }

        // `channels_value` should be a CFArrayRef of channel dictionaries.
        CFArrayRef channels_array = static_cast<CFArrayRef>(channels_value);
        CFIndex array_count = CFArrayGetCount(channels_array);

        // Iterate through all channels in our subscription.
        for (CFIndex i = 0; i < array_count; i++) {
            const void* item_ptr = CFArrayGetValueAtIndex(channels_array, i);
            CFDictionaryRef item = static_cast<CFDictionaryRef>(item_ptr);

            // Get the channel's name and unit label.
            CFStringRef cf_channel_name = IOReportChannelGetChannelName(item);
            CFStringRef cf_unit = IOReportChannelGetUnitLabel(item);

            std::string channel_name = to_std_string(cf_channel_name);
            int64_t energy = IOReportSimpleGetIntegerValue(item, 0);
            std::string unit = to_std_string(cf_unit);

            energy = convert_to_mj(energy, unit);

            if (channel_name.find("CPU Energy") != std::string::npos) {
                result.cpu_total_mj = energy;
            } else if (is_cpu_core(channel_name, 'E')) {
                if (!result.efficiency_cores_mj) {
                    result.efficiency_cores_mj = std::vector<int64_t>();
                }
                result.efficiency_cores_mj->push_back(energy);
            } else if (is_cpu_core(channel_name, 'P')) {
                if (!result.performance_cores_mj) {
                    result.performance_cores_mj = std::vector<int64_t>();
                }
                result.performance_cores_mj->push_back(energy);
            } else if (is_cpu_manager(channel_name, 'E')) {
                result.efficiency_core_manager_mj = result.efficiency_core_manager_mj.value_or(0) + energy;
            } else if (is_cpu_manager(channel_name, 'P')) {
                result.performance_core_manager_mj = result.performance_core_manager_mj.value_or(0) + energy;
            } else if (channel_name.find("DRAM") != std::string::npos) {
                result.dram_mj = result.dram_mj.value_or(0) + energy;
            } else if (channel_name.find("GPU Energy") != std::string::npos) {
                result.gpu_mj = energy;
            } else if (channel_name.find("GPU SRAM") != std::string::npos) {
                result.gpu_sram_mj = result.gpu_sram_mj.value_or(0) + energy;
            } else if (channel_name.find("ANE") != std::string::npos) {
                result.ane_mj = result.ane_mj.value_or(0) + energy;
            }
        }

        return result;
    }

    std::string to_std_string(CFStringRef cf_str)
    {
        char buffer[256];
        bool ok = CFStringGetCString(cf_str, buffer, sizeof(buffer),
            kCFStringEncodingUTF8);
        if (ok) {
            return std::string(buffer);
        }
        throw std::runtime_error("Failed to convert CFString to std::string");
    }

    // Checks if a string starts with `core_type` and ends with "CPU" followed by
    // a number.
    bool is_cpu_core(const std::string& s, char core_type)
    {
        // 1) Check first character.
        if (s.empty() || s[0] != core_type) {
            return false;
        }

        // 2) Find the last occurrence of "CPU"
        std::size_t pos = s.rfind("CPU");
        if (pos == std::string::npos) {
            return false;
        }

        // Ensure there's at least one character after "CPU" (for the number)
        std::size_t startOfNumber = pos + 3;
        if (startOfNumber >= s.size()) {
            return false;
        }

        // 3) Verify that all remaining characters are digits
        for (std::size_t i = startOfNumber; i < s.size(); ++i) {
            if (!std::isdigit(static_cast<unsigned char>(s[i]))) {
                return false;
            }
        }

        return true;
    }

    // Checks if a string starts with `core_type` and ends with "CPM".
    bool is_cpu_manager(const std::string& s, char core_type)
    {
        // 1) Check first character.
        if (s.empty() || s[0] != core_type) {
            return false;
        }

        // 2) Check if the string ends with "CPM".
        if (s.size() < 3 || s.compare(s.size() - 3, 3, "CPM") != 0) {
            return false;
        }

        return true;
    }

    int64_t convert_to_mj(int64_t energy, const std::string& unit)
    {
        if (unit == "nJ") {
            return energy / 1'000'000LL;
        } else if (unit == "uJ" || unit == "µJ") {
            return energy / 1'000LL;
        } else if (unit == "mJ") {
            return energy;
        } else if (unit == "cJ") {
            return energy * 10LL;
        } else if (unit == "dJ") {
            return energy * 100LL;
        } else if (unit == "J") {
            return energy * 1'000LL;
        } else if (unit == "daJ") {
            return energy * 10'000LL;
        } else if (unit == "hJ") {
            return energy * 100'000LL;
        } else if (unit == "kJ") {
            return energy * 1'000'000LL;
        } else if (unit == "MJ") {
            return energy * 1'000'000'000LL;
        } else if (unit == "GJ") {
            return energy * 1'000'000'000'000LL;
        } else if (unit == "TJ") {
            return energy * 1'000'000'000'000'000LL;
        } else if (unit == "PJ") {
            return energy * 1'000'000'000'000'000'000LL;
        } else {
            throw std::invalid_argument("Unsupported or invalid energy unit provided: " + unit);
        }
    }
};
