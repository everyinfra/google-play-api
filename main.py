"""Google Play API 示例（Google Play API in Python）。

  python main.py search "note taking" --out apps.csv  # 按关键词搜应用 / search apps
  python main.py app <应用包名> --out app.json        # 应用详情 / app detail
  python main.py reviews <应用包名> --out reviews.csv # 应用评价 / reviews
"""
import argparse

from everyinfra import fetch, report

SORTS = ["newest", "top_rated"]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="按关键词搜应用 / search apps by keyword")
    s.add_argument("keyword")
    s.add_argument("--country", help="店面国家，默认 us / store country, default us")
    ap = sub.add_parser("app", help="应用详情 / one app")
    ap.add_argument("app_id")
    r = sub.add_parser("reviews", help="应用评价 / reviews of one app")
    r.add_argument("app_id")
    r.add_argument("--sort", choices=SORTS, help="newest 最新 / top_rated 评分较高")
    for x in (s, r):
        x.add_argument("--pages", type=int, default=1, help="最多翻几页，每页算一次调用 / max pages, one call each")
    for x in (s, ap, r):
        x.add_argument("--out", help="存成 .csv 或 .json / write .csv or .json")
    a = p.parse_args()

    if a.cmd == "search":
        params = {"keyword": a.keyword, **({"country": a.country} if a.country else {})}
        rows, charged = fetch("search", params, a.pages)
    elif a.cmd == "app":
        rows, charged = fetch("profile", {"app_id": a.app_id})
    else:
        params = {"app_id": a.app_id, **({"sort": a.sort} if a.sort else {})}
        rows, charged = fetch("reviews", params, a.pages)
    report(rows, charged, a.out)


if __name__ == "__main__":
    main()
