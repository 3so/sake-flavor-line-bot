import get_sakenowa_api as gs
import flavor_chart as fc

#銘柄リストの返却

def search_brand(event):
    search_word = event.message.text
    search_brands = gs.search_brands(search_word)

    # 該当する銘柄が1件だった場合
    if len(search_brands) == 1:
        searched_brand = search_brands[0]
        flavor = gs.get_flavor(searched_brand)
        # フレーバー情報がある場合
        if flavor["flavorIs?"] == "true":
            fc.get_flavor_chart(flavor)
            return 0, flavor["brandName"]
        # フレーバー情報がない場合
        else:
            return 1, flavor["brandName"]

    # 検索ワードに一致する銘柄がない場合、その旨を返却
    elif len(search_brands) == 0:
        return 2, "" # "該当する銘柄が見つかりませんでした。"

    # 候補が多すぎる場合、その旨を返却
    elif len(search_brands) >= 31:
        return 3, ""

    # 銘柄数が30以下の場合、銘柄リストを返却
    elif len(search_brands) <= 30:
        brand_list = ""
        for brand in search_brands:
            brand_list += brand["name"] + "\n"
        brand_list = brand_list.rstrip()
        return 4, brand_list