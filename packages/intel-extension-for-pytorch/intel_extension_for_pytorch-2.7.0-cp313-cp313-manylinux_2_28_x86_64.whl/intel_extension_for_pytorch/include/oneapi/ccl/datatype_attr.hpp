/*
 Copyright 2016-2020 Intel Corporation
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
     http://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/
#pragma once

#ifndef CCL_PRODUCT_FULL
#error "Do not include this file directly. Please include 'ccl.hpp'"
#endif

namespace ccl {
namespace detail {
class environment;
}

class ccl_datatype_attr_impl;

namespace v1 {

class datatype_attr : public ccl_api_base_copyable<datatype_attr,
                                                   copy_on_write_access_policy,
                                                   ccl_datatype_attr_impl> {
public:
    using base_t =
        ccl_api_base_copyable<datatype_attr, copy_on_write_access_policy, ccl_datatype_attr_impl>;

    /**
     * Declare PIMPL type
     */
    using impl_value_t = typename base_t::impl_value_t;

    /**
     * Declare implementation type
     */
    using impl_t = typename impl_value_t::element_type;

    datatype_attr& operator=(const datatype_attr& src);
    datatype_attr& operator=(datatype_attr&& src);
    datatype_attr(datatype_attr&& src);
    datatype_attr(const datatype_attr& src);
    ~datatype_attr() noexcept;

    /**
     * Set specific value for selft attribute by @attrId.
     * Previous attibute value would be returned
     */
    template <datatype_attr_id attrId,
              class Value/*,
              class = typename std::enable_if<is_attribute_value_supported<attrId, Value>()>::return_type*/>
    Value set(const Value& v);

    /**
     * Get specific attribute value by @attrId
     */
    template <datatype_attr_id attrId>
    const typename detail::ccl_api_type_attr_traits<datatype_attr_id, attrId>::return_type& get()
        const;

private:
    friend class ccl::detail::environment;
    datatype_attr(
        const typename detail::ccl_api_type_attr_traits<datatype_attr_id,
                                                        datatype_attr_id::version>::return_type&
            version);
};

template <datatype_attr_id t, class value_type>
constexpr auto attr_val(value_type v)
    -> detail::attr_value_triple<datatype_attr_id, t, value_type> {
    return detail::attr_value_triple<datatype_attr_id, t, value_type>(v);
}

} // namespace v1

using v1::datatype_attr;
using v1::attr_val;

} // namespace ccl
