#!/usr/bin/env bash

# 遇到执行出错，直接终止脚本的执行
set -o errexit

logger_print()
{
    local prefix="[$(date +%Y/%m/%d\ %H:%M:%S)]"
    echo "${prefix}$@" >&2
}

function test_rpc_methods
{

    grpcurl -rpc-header x-request-id:73338239da584998aca91639651334fa -d @ -plaintext localhost:{{ServicePort}} {{ServiceNameInUnderScoreCase}}.{{ServiceNameInCamelCase}}/Ping << EOM
{
}
EOM

}

function run
{
    grpcurl -plaintext localhost:{{ServicePort}} list {{ServiceNameInUnderScoreCase}}.{{ServiceNameInCamelCase}}
    test_rpc_methods
}

run $@
