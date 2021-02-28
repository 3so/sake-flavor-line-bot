import get_sakenowa_api as gs
import flavor_chart as fc

#銘柄リストの返却

def search_brand(event):
    search_word = event.message.text
    search_brands = gs.search_brands(search_word)

    # 該当する銘柄が1件だった場合
    if len(search_brands) == 1:
        # フレーバー情報の取得
        searched_brand = search_brands[0]
        # フレーバー情報の取得
        flavor = gs.get_flavor(searched_brand)
        # フレーバータグの取得
        flavor_tags = gs.get_flavor_tags(searched_brand["id"])
        # フレーバー情報がある場合
        if flavor["flavorIs?"] == "true":
            fc.get_flavor_chart(flavor)
            # フレーバータグがある場合
            if flavor_tags != []:
                return 0, 0, flavor["brandName"], flavor_tags
            # フレーバータグがない場合
            else:
                return 0, 1, flavor["brandName"]
        # フレーバー情報がない場合
        else:
            # フレーバータグがある場合
            if flavor_tags != []:
                return 1, 0, flavor["brandName"], flavor_tags
            # フレーバータグがない場合
            else:
                return 1, 1, flavor["brandName"]

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