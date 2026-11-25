#!/usr/bin/env bash
# Google Play API 的 curl 示例：所有能力都发到同一个地址，只换 action 和 params。
# curl examples for the Google Play API: every capability uses the same URL; only action and params change.
#
#   export EVERYINFRA_API_KEY=<your API key>
#   bash examples/curl.sh search "note taking"
#   bash examples/curl.sh profile <package name> # search 结果里的 app_id，即包名 / the app_id (package name) from a search result
#   bash examples/curl.sh reviews <package name>
#
# 翻页：把响应里的 next_page_token 放进 params.page_token 再调一次，每页算一次调用。
# Next page: send the response's next_page_token back as params.page_token. Each page is one call.
set -euo pipefail
: "${EVERYINFRA_API_KEY:?Set EVERYINFRA_API_KEY first: https://everyinfra.com/docs#quickstart}"
action=${1:?"usage: bash examples/curl.sh <search|profile|reviews> <value>"}
value=${2:?"value: a keyword or a package name"}

case "$action" in
  search)            params="{\"keyword\":\"$value\"}" ;;
  profile | reviews) params="{\"app_id\":\"$value\"}" ;;
  *) echo "unknown action: $action (use search, profile or reviews)" >&2; exit 2 ;;
esac

curl -sS -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"platform\":\"google_play\",\"action\":\"$action\",\"params\":$params}"
echo
