#!/bin/bash
#
# Copyright 2016-2020 Intel Corporation
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# shellcheck shell=sh

DEFAULT_BUNDLED_MPI="yes"

get_script_path() (
    script="$1"
    while [ -L "$script" ] ; do
        # combining next two lines fails in zsh shell
        script_dir=$(command dirname -- "$script")
        script_dir=$(cd "$script_dir" && command pwd -P)
        script="$(readlink "$script")"
        case $script in
            (/*) ;;
            (*) script="$script_dir/$script" ;;
        esac
    done
    # combining next two lines fails in zsh shell
    script_dir=$(command dirname -- "$script")
    script_dir=$(cd "$script_dir" && command pwd -P)
    printf "%s" "$script_dir"
)

_vars_get_proc_name() {
    if [ -n "${ZSH_VERSION:-}" ] ; then
        script="$(ps -p "$$" -o comm=)"
    else
        script="$1"
        while [ -L "$script" ] ; do
            script="$(readlink "$script")"
        done
    fi
    basename -- "$script"
}

_vars_this_script_name="vars.sh"
if [ "$_vars_this_script_name" = "$(_vars_get_proc_name "$0")" ] ; then
    echo "   ERROR: Incorrect usage: this script must be sourced."
    echo "   Usage: . path/to/${_vars_this_script_name}"
    return 255 2>/dev/null || exit 255
fi

prepend_path() (
  path_to_add="$1"
  path_is_now="$2"

  if [ "" = "${path_is_now}" ] ; then   # avoid dangling ":"
    printf "%s" "${path_to_add}"
  else
    printf "%s" "${path_to_add}:${path_is_now}"
  fi
)

vars_script_name=""
vars_script_shell="$(ps -p "$$" -o comm=)"

if [ -n "${ZSH_VERSION:-}" ] && [ -n "${ZSH_EVAL_CONTEXT:-}" ] ; then
    case $ZSH_EVAL_CONTEXT in (*:file*) vars_script_name="${(%):-%x}" ;; esac ;
elif [ -n "${KSH_VERSION:-}" ] ; then
    if [ "$(set | grep -Fq "KSH_VERSION=.sh.version" ; echo $?)" -eq 0 ] ; then
        vars_script_name="${.sh.file}" ;
    else
        vars_script_name="$( (echo "${.sh.file}") 2>&1 )" || : ;
        vars_script_name="$(expr "${vars_script_name:-}" : '^.*sh: \(.*\)\[[0-9]*\]:')" ;
    fi
elif [ -n "${BASH_VERSION:-}" ] ; then
    (return 0 2>/dev/null) && vars_script_name="${BASH_SOURCE}" ;
elif [ "dash" = "$vars_script_shell" ] ; then
    vars_script_name="$( (echo "${.sh.file}") 2>&1 )" || : ;
    vars_script_name="$(expr "${vars_script_name:-}" : '^.*dash: [0-9]*: \(.*\):')" ;
elif [ "sh" = "$vars_script_shell" ] ; then
    vars_script_name="$( (echo "${.sh.file}") 2>&1 )" || : ;
    if [ "$(printf "%s" "$vars_script_name" | grep -Eq "sh: [0-9]+: .*vars\.sh: " ; echo $?)" -eq 0 ] ; then
        vars_script_name="$(expr "${vars_script_name:-}" : '^.*sh: [0-9]*: \(.*\):')" ;
    fi
else
    vars_script_name="$( (echo "${.sh.file}") 2>&1 )" || : ;
    if [ "$(printf "%s" "$vars_script_name" | grep -Eq "^.+: [0-9]+: .*vars\.sh: " ; echo $?)" -eq 0 ] ; then # dash
        vars_script_name="$(expr "${vars_script_name:-}" : '^.*: [0-9]*: \(.*\):')" ;
    else
        vars_script_name="" ;
    fi
fi

if [ "" = "$vars_script_name" ] ; then
    >&2 echo "   ERROR: Unable to proceed: possible causes listed below."
    >&2 echo "   This script must be sourced. Did you execute or source this script?" ;
    >&2 echo "   Unrecognized/unsupported shell (supported: bash, zsh, ksh, m/lksh, dash)." ;
    >&2 echo "   May fail in dash if you rename this script (assumes \"vars.sh\")." ;
    >&2 echo "   Can be caused by sourcing from ZSH version 4.x or older." ;
    return 255 2>/dev/null || exit 255
fi

WORK_DIR=$(get_script_path "${vars_script_name:-}")

CCL_ROOT="$(cd "${WORK_DIR}"/../; pwd -P)"; export CCL_ROOT

CPATH=$(prepend_path "${CCL_ROOT}/include" "${CPATH:-}"); export CPATH
CMAKE_PREFIX_PATH=$(prepend_path "${CCL_ROOT}/lib/cmake/oneCCL" "${CMAKE_PREFIX_PATH:-}"); export CMAKE_PREFIX_PATH
LIBRARY_PATH=$(prepend_path "${CCL_ROOT}/lib" "${LIBRARY_PATH:-}"); export LIBRARY_PATH
LD_LIBRARY_PATH=$(prepend_path "${CCL_ROOT}/lib" "${LD_LIBRARY_PATH:-}"); export LD_LIBRARY_PATH

args=$*
for arg in $args
do
    case "$arg" in
        --ccl-bundled-mpi=*)
            ccl_bundled_mpi="${arg#*=}"
            ;;
    esac
done

if [ -z "${SETVARS_CALL:-}" ] ; then
    if [ -z "${ccl_bundled_mpi:-}" ]; then
        ccl_bundled_mpi="${DEFAULT_BUNDLED_MPI}"
    elif [ "$ccl_bundled_mpi" != "yes" ] && [ "$ccl_bundled_mpi" != "no" ]; then
        echo ":: WARNING: ccl_bundled_mpi=${ccl_bundled_mpi} is unrecognized."
        echo ":: ccl_bundled_mpi will be set to ${DEFAULT_BUNDLED_MPI}"
        ccl_bundled_mpi="${DEFAULT_BUNDLED_MPI}"
    fi

    if [ "$ccl_bundled_mpi" = "yes" ] ; then
        export I_MPI_ROOT="${CCL_ROOT}/opt/mpi"
        CPATH=$(prepend_path "${I_MPI_ROOT}/include" "${CPATH:-}"); export CPATH
        LD_LIBRARY_PATH=$(prepend_path "${I_MPI_ROOT}/lib" "${LD_LIBRARY_PATH:-}") ; export LD_LIBRARY_PATH
        LIBRARY_PATH=$(prepend_path "${I_MPI_ROOT}/lib" "${LIBRARY_PATH:-}"); export LIBRARY_PATH
        PATH="${I_MPI_ROOT}/bin:${PATH}"; export PATH
    fi
else
    if [ ! -z "${ccl_bundled_mpi:-}" ]; then
        echo ":: WARNING: ccl_bundled_mpi was specified for setvars.sh script"
        echo ":: ccl_bundled_mpi is only supported by direct call vars.sh, ignoring"
    fi
fi
