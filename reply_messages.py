import get_sakenowa_api as gs

def brand_list(event):
    search_word = event.message.text
    search_word = search_word.replace("\\n","")
    search_brands = gs.search_brands(event.message.text)
    if search_brands == []:
        return "該当する銘柄が見つかりませんでした"
    else:
        brand_list = ""
        for brand in search_brands:
            brand_list += brand["name"] + "\n"
        return brand_list
