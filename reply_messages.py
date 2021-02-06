import get_sakenowa_api as gs

#銘柄リストの返却

def brand_list(event):
    search_word = event.message.text
    search_brands = gs.search_brands(search_word)

    # 検索ワードに一致する銘柄がない場合、その旨を返却
    if search_brands == []:
        return "該当する銘柄が見つかりませんでした"

    # 候補が多すぎる場合、その旨を返却
    elif len(search_brands) > 30:
        return "該当する銘柄が多すぎます。別の検索ワードをお試しください。"

    # 銘柄数が30以下の場合、銘柄リストを返却
    else:
        brand_list = ""
        for brand in search_brands:
            brand_list += brand["name"] + "\n"
        return brand_list
