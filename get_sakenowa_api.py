import requests
import json

urls = {
    "地域一覧": "https://muro.sakenowa.com/sakenowa-data/api/areas",
    "銘柄一覧": "https://muro.sakenowa.com/sakenowa-data/api/brands",
    "蔵元一覧": "https://muro.sakenowa.com/sakenowa-data/api/breweries",
    "ランキング": "https://muro.sakenowa.com/sakenowa-data/api/rankings",
    "フレーバー情報": "https://muro.sakenowa.com/sakenowa-data/api/flavor-charts",
    "フレーバータグ": "https://muro.sakenowa.com/sakenowa-data/api/flavor-tags",
    "銘柄ごとフレーバータグ": "https://muro.sakenowa.com/sakenowa-data/api/brand-flavor-tags",
    }

def get_area():
    url = urls["地域一覧"]
    responce_areas = requests.get(url).json()
    return responce_areas["areas"]

def get_breweries(area_id):
    url = urls["蔵元一覧"]
    responce_breweries = requests.get(url).json()
    breweries = responce_breweries["breweries"]
    selected_breweries = []
    for brewery in breweries:
        if brewery["areaId"] == area_id:
            if brewery["name"] != "":
                selected_breweries.append(brewery)
            else:
                brewery["name"] = "その他酒蔵"
                selected_breweries.append(brewery)
    if selected_breweries == []:
        return [{"id":"","name":"------","areaId":""}]
    else:
        selected_breweries.insert(0, {"id":"","name":"選択してください","areaId":""})
        return selected_breweries

def get_brands(brewery_id):
    url = urls["銘柄一覧"]
    responce_brands = requests.get(url).json()
    brands = responce_brands["brands"]
    selected_brands = []
    for brand in brands:
        if brand["breweryId"] == brewery_id:
            selected_brands.append(brand)
    if selected_brands == []:
        return [{"id":"","name":"------","breweryId":""}]
    else:
        selected_brands.insert(0, {"id":"","name":"選択してください","breweryId":""})
        return selected_brands

def get_flavor(brand):
    url = urls["フレーバー情報"]
    responce_flavors = requests.get(url).json()
    flavors = responce_flavors["flavorCharts"]
    brand_id = brand["id"]
    brand_name = brand["name"]
    for flavor in flavors:
        if flavor["brandId"] == brand_id:
            flavor["flavorIs?"] = "true"
            flavor["brandName"] = brand_name
            return flavor
    return { "brandId":brand_id, "brandName":brand_name, "flavorIs?":"false"}

# 引用元そのまま
# def get_flavors(brand_id, brands):
#    url = urls["フレーバー情報"]
#    responce_flavors = requests.get(url).json()
#    flavors = responce_flavors["flavorCharts"]
#    brand_name = ""
#    for brand in brands:
#        if brand["id"] == brand_id:
#            brand_name = brand["name"]
#    for flavor in flavors:
#        if flavor["brandId"] == brand_id:
#            flavor["flavor"] = "true"
#            flavor["brandName"] = brand_name
#            return flavor
#    return { "brandId":brand_id, "brandName":brand_name, "flavor":""}

def get_flavor_tags(brand_id):
    url = urls["フレーバータグ"]
    responce_flavor_tags = requests.get(url).json()
    flavor_tags = responce_flavor_tags["tags"]
    url = urls["銘柄ごとフレーバータグ"]
    responce_brand_flavor_tags = requests.get(url).json()
    brand_flavor_tags = responce_brand_flavor_tags["flavorTags"]
    selected_brand_flavor_tag = { "brandId" : brand_id }
    tag_names = []
    for bland_flavor_tag in brand_flavor_tags:
        if bland_flavor_tag["brandId"] == brand_id:
            for tag in bland_flavor_tag["tagIds"]:
                for flavor_tag in flavor_tags:
                    if tag == flavor_tag["id"]:
                        tag_names.append(flavor_tag["tag"])
            selected_brand_flavor_tag["tag_names"] = tag_names
            return selected_brand_flavor_tag

def search_brands(input_text):
    url = urls["銘柄一覧"]
    responce_brands = requests.get(url).json()
    brands = responce_brands["brands"]
    search_brands = []
    for brand in brands:
        if input_text in brand["name"]:
            search_brands.append(brand)
    return search_brands