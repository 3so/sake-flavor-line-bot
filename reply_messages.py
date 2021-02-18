import get_sakenowa_api as gs

#銘柄リストの返却

def search_brand(event):
    search_word = event.message.text
    search_brands = gs.search_brands(search_word)

    # 検索ワードに一致する銘柄がない場合、その旨を返却
    if len(search_brands) == 0:
        return 0, "" # "該当する銘柄が見つかりませんでした。"

    # 候補が多すぎる場合、その旨を返却
    elif len(search_brands) >= 31:
        return 1, ""

    # 銘柄数が30以下の場合、銘柄リストを返却
    elif len(search_brands) <= 30:
        brand_list = ""
        for brand in search_brands:
            brand_list += brand["name"] + "\n"
        brand_list = brand_list.rstrip()
        return 2, brand_list

    # 該当する銘柄が1件だった場合、フレーバー情報を返却
    elif len(search_brands) == 1:
        search_brand = search_brands[0]
        return 3, search_brand["name"]