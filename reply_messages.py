import get_sakenowa_api as gs

#銘柄リストの返却

def search_brand(event):
    search_word = event.message.text
    search_brands = gs.search_brands(search_word)

    # 検索ワードに完全一致する銘柄があった場合、フレーバー情報を返却
    if len(search_brands) == 1:
        search_brand = search_brands[0]
        return 0, search_brand["name"]

    # 検索ワードに一致する銘柄がない場合、その旨を返却
    elif len(search_brands) == 0:
        return 1, "" # "該当する銘柄が見つかりませんでした。"

    # 候補が多すぎる場合、その旨を返却
    elif len(search_brands) >= 31:
        return 2, ""

    # 銘柄数が30以下の場合、銘柄リストを返却
    elif len(search_brands) <= 30:
        brand_list = ""
        for brand in search_brands:
            brand_list += brand["name"] + "\n"
        return 3, brand_list
