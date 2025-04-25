#include "ioreport_mocker.hpp"
#include <CoreFoundation/CoreFoundation.h>
#include <cassert>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

/* ----- Variables and functions for mock data input configuration ----- */
static std::vector<const std::unordered_map<std::string, std::pair<int64_t, std::string>>> sample_data;
static uint64_t mock_sample_index = 0;

Mocker::Mocker()
{
    mock_sample_index = 0;
}

Mocker::~Mocker()
{
    clear_all_mock_samples();
    mock_sample_index = 0;
}

void Mocker::push_back_sample(const std::unordered_map<std::string, std::pair<int64_t, std::string>>& data)
{
    sample_data.push_back(data);
}

void Mocker::pop_back_sample()
{
    if (sample_data.empty()) {
        throw std::out_of_range("No more mock samples to pop");
    }
    sample_data.pop_back();
}

void Mocker::clear_all_mock_samples()
{
    sample_data.clear();
}

void Mocker::set_sample_index(uint64_t index)
{
    if (index < 0 || index >= sample_data.size()) {
        throw std::out_of_range("Sample index out of range");
    }
    mock_sample_index = index;
}

/* ----- Forward declarations to functions we'll be mocking ----- */
extern "C" {
typedef struct __IOReportSubscriptionRef* IOReportSubscriptionRef;

/* Note that we forward-declare these because some of them use/need each other.
 */
CFDictionaryRef IOReportCopyChannelsInGroup(CFStringRef group,
    CFStringRef subgroup, uint64_t a,
    uint64_t b, uint64_t c);

IOReportSubscriptionRef IOReportCreateSubscription(
    const void* unused1, CFMutableDictionaryRef channels_dict,
    CFMutableDictionaryRef* unused2, uint64_t unused3, CFTypeRef unused4);

CFDictionaryRef IOReportCreateSamples(IOReportSubscriptionRef subs,
    CFMutableDictionaryRef channels_dict_mut,
    const void* unused);

CFDictionaryRef IOReportCreateSamplesDelta(CFDictionaryRef sample1,
    CFDictionaryRef sample2,
    const void* unused);

int64_t IOReportSimpleGetIntegerValue(CFDictionaryRef item, int unused);

CFStringRef IOReportChannelGetChannelName(CFDictionaryRef item);

CFStringRef IOReportChannelGetUnitLabel(CFDictionaryRef item);
}

/* ----- Helper functions and variables ----- */

/* Constants that we use when key-ing across different dictionaries. */
static const CFStringRef kMockKeyChannelName = CFSTR("MockInternalChannelName");
static const CFStringRef kMockKeyUnitLabel = CFSTR("MockInternalUnitLabel");
static const CFStringRef kMockKeyValue = CFSTR("MockInternalValue");

std::string to_std_string(CFStringRef cf_str)
{
    char buffer[256];
    bool ok = CFStringGetCString(cf_str, buffer, sizeof(buffer), kCFStringEncodingUTF8);
    if (ok) {
        return std::string(buffer);
    }
    throw std::runtime_error("Failed to convert CFString to std::string");
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

CFDictionaryRef create_mock_channel_item(const std::string& name, int64_t value, const std::string& unit)
{
    CFStringRef cf_name = CFStringCreateWithCString(nullptr, name.c_str(), kCFStringEncodingUTF8);

    CFStringRef cf_unit = CFStringCreateWithCString(nullptr, unit.c_str(), kCFStringEncodingUTF8);
    CFNumberRef cf_value = CFNumberCreate(nullptr, kCFNumberSInt64Type, &value);

    const void* keys[] = { kMockKeyChannelName, kMockKeyUnitLabel, kMockKeyValue };
    const void* values[] = { cf_name, cf_unit, cf_value };

    CFDictionaryRef channel_dict = CFDictionaryCreate(
        nullptr, keys, values, sizeof(keys) / sizeof(keys[0]),
        &kCFTypeDictionaryKeyCallBacks, &kCFTypeDictionaryValueCallBacks);

    CFRelease(cf_name);
    CFRelease(cf_unit);
    CFRelease(cf_value);

    return channel_dict;
}

CFDictionaryRef create_sample_from_config(
    const std::unordered_map<std::string, std::pair<int64_t, std::string>>& config)
{
    std::vector<CFTypeRef> channel_items;
    channel_items.reserve(config.size());

    for (const auto& pair : config) {
        const std::string& channel_name = pair.first;
        int64_t value = pair.second.first;
        const std::string& unit = pair.second.second;

        CFDictionaryRef item = create_mock_channel_item(channel_name, value, unit);
        channel_items.push_back(item);
    }

    CFArrayRef channels_array = CFArrayCreate(nullptr, channel_items.data(), channel_items.size(),
        &kCFTypeArrayCallBacks);

    for (CFTypeRef item : channel_items) {
        CFRelease(item);
    }

    CFStringRef key = CFSTR("IOReportChannels");
    const void* keys[] = { key };
    const void* values[] = { channels_array };
    CFDictionaryRef sample_dict = CFDictionaryCreate(
        nullptr, keys, values, 1, &kCFTypeDictionaryKeyCallBacks,
        &kCFTypeDictionaryValueCallBacks);

    CFRelease(channels_array);

    return sample_dict;
}

/* Parses a sample object and returns a hashmap containing its fields. */
const std::unordered_map<std::string, std::pair<int64_t, std::string>> parse_sample(CFDictionaryRef sample)
{
    std::unordered_map<std::string, std::pair<int64_t, std::string>> result;

    CFStringRef key_str = CFStringCreateWithCString(nullptr, "IOReportChannels",
        kCFStringEncodingUTF8);
    const void* channels_value = CFDictionaryGetValue(sample, key_str);
    CFRelease(key_str);

    assert(channels_value != nullptr);

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
        std::string unit = to_std_string(cf_unit);
        int64_t energy = IOReportSimpleGetIntegerValue(item, 0);

        result[channel_name] = std::make_pair(energy, unit);
    }

    return result;
}

/* ----- Mock Implementations of IOReport Functions ----- */

extern "C" {

/* Returns an empty dictionary; since we're mocking, this is okay. */
CFDictionaryRef IOReportCopyChannelsInGroup(CFStringRef group,
    CFStringRef subgroup, uint64_t a,
    uint64_t b, uint64_t c)
{
    return CFDictionaryCreate(nullptr, nullptr, nullptr, 0,
        &kCFTypeDictionaryKeyCallBacks,
        &kCFTypeDictionaryValueCallBacks);
}

/* Returns a pointer to a not-real subscription. */
IOReportSubscriptionRef IOReportCreateSubscription(
    const void* unused1, CFMutableDictionaryRef channels_dict,
    CFMutableDictionaryRef* unused2, uint64_t unused3, CFTypeRef unused4)
{

    // The reason we can't just return a random non-null C-pointer is because
    // the monitor will try to release it; so, we need to return a kCFNull
    // instead, which is a null-like value that doesn't cause problems
    // when released.
    return (IOReportSubscriptionRef)kCFNull;
}

/* Creates a mock sample based on configured data. */
CFDictionaryRef IOReportCreateSamples(IOReportSubscriptionRef subs,
    CFMutableDictionaryRef channels_dict_mut,
    const void* unused)
{
    if (mock_sample_index >= sample_data.size()) {
        throw std::out_of_range("No more mock samples available");
    }
    return create_sample_from_config(sample_data[mock_sample_index++]);
}

/* Creates a sample containing the diff of two input samples. */
CFDictionaryRef IOReportCreateSamplesDelta(CFDictionaryRef sample1,
    CFDictionaryRef sample2,
    const void* unused)
{
    std::unordered_map<std::string, std::pair<int64_t, std::string>> diff_data;

    const std::unordered_map<std::string, std::pair<int64_t, std::string>> sample1_data = parse_sample(sample1);
    const std::unordered_map<std::string, std::pair<int64_t, std::string>> sample2_data = parse_sample(sample2);

    for (const auto& pair : sample2_data) {
        const std::string& key = pair.first;

        auto it = sample1_data.find(key);
        if (it == sample1_data.end()) {
            diff_data[key] = pair.second;
            continue;
        }

        int64_t value1 = it->second.first;
        int64_t value2 = pair.second.first;

        std::string unit1 = it->second.second;
        std::string unit2 = pair.second.second;

        if (unit1 == unit2) {
            diff_data[key] = std::make_pair(value2 - value1, unit1);
        } else {
            diff_data[key] = std::make_pair(
                convert_to_mj(value2, unit2) - convert_to_mj(value1, unit1), "mJ");
        }
    }

    return create_sample_from_config(diff_data);
}

/* Returns integer value from mock channel item dictionary. */
int64_t IOReportSimpleGetIntegerValue(CFDictionaryRef item, int unused)
{
    if (!item)
        return 0;
    CFNumberRef cf_value = (CFNumberRef)CFDictionaryGetValue(item, kMockKeyValue);
    if (!cf_value)
        return 0;
    int64_t value = 0;
    CFNumberGetValue(cf_value, kCFNumberSInt64Type, &value);
    return value;
}

/* Returns channel name string from mock channel item dictionary. */
CFStringRef IOReportChannelGetChannelName(CFDictionaryRef item)
{
    if (!item)
        return nullptr;
    return (CFStringRef)CFDictionaryGetValue(item, kMockKeyChannelName);
}

/* Returns unit label string from mock channel item dictionary. */
CFStringRef IOReportChannelGetUnitLabel(CFDictionaryRef item)
{
    if (!item)
        return nullptr;
    return (CFStringRef)CFDictionaryGetValue(item, kMockKeyUnitLabel);
}
}
