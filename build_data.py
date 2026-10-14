"""產生故事地圖原型用的 GeoJSON（EPSG:4326）。
road_agg：66 年名冊按路名分組的圓圈（來源 glass_1977_road_agg.gpkg）
factories：合成／華夏、新生 66/82 年點位。
  - 66 年取自 glass_1977.gpkg（定位精度低）或公開資料記載的地址；
  - 82 年名冊只有地址，這裡用 OSM 路段位置概略標示（非門牌座標），precision 欄已註明。
名冊比對（2026-10-08）：66 年名冊只有「合成玻璃工廠」，沒有「華夏」；82 年名冊「合成」(東南街53巷16號, 60人) 與
「華夏玻璃股份有限公司」(牛埔路93巷49號, 539人) 並列。華夏官網沿革確認華夏即合成（1925 合成 → 聯成 → 1974 華夏），
名冊並列的原因未查證。
"""
import json, os
import geopandas as gpd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = r"D:\專案管理\a008_新竹玻璃\03_地圖"
agg = gpd.read_file(os.path.join(ROOT, "密度圖", "glass_1977_road_agg.gpkg"), layer="road_agg").to_crs(4326)
agg = agg[["label", "n", "geometry"]].copy()
agg.to_file(os.path.join(HERE, "data", "road_agg.geojson"), driver="GeoJSON")

pts = gpd.read_file(os.path.join(ROOT, "佩瑾產圖", "glass_1977.gpkg"), layer="points_unique").to_crs(4326)
def p66(name):
    r = pts[pts["name"] == name].iloc[0]
    return r.geometry.y, r.geometry.x, r.addr_1977, r.geocode_level

feat = []
def add(fid, grp, label, year, lat, lon, addr, precision, product, staff, note):
    feat.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [lon, lat]},
                 "properties": dict(id=fid, grp=grp, label=label, year=year, addr=addr, precision=precision,
                                    product=product, staff=staff, note=note)})

# 合成／華夏。名冊的 頂竹里 地名點在 glass_1977.gpkg 落在(121.0065,24.787)，與 OSM 的頂竹里(約 120.973,24.799)差約 3 km，
# 故 66 年合成改用 82 年名冊同址「東南街53巷16號」之 OSM 路段位置（官網與國家文化記憶庫記載的原址）。
add("hs66", "hs", "合成玻璃・民國66、82年", 1977, 24.7994, 120.9742,
    "頂竹里東南街53巷16號（66年名冊寫頂竹里頂竹2號）", "路段概略", "電表蓋、玻璃殼（82年）", 60, "66年名冊寫頂竹里頂竹2號、82年寫東南街53巷16號；位置依82年地址與國家文化記憶庫記載的原址")
add("hx82", "hs", "華夏玻璃・民國82年", 1993, 24.7963, 120.9393,
    "牛埔路93巷49號", "路段概略", "小型瓶、玻璃壓製器具", 539, "民82年名錄（另一列「華夏玻璃工業公司」寫牛埔南路93巷49號；座標取牛埔南路路段）；66年名冊無此名")

# 新生高級玻璃。66 年名冊寫「香山鄉松樹腳2號」，glass_1977.gpkg 依林松陳口述以牛埔里定位（村里級）。
la, lo, ad, pr = p66("新生高級玻璃工廠")
add("xs66", "xs", "新生高級玻璃・民國66年", 1977, la, lo, ad, pr, "", "", "名冊列「新生高級玻璃工廠」，村里級定位")
add("xs82", "xs", "新生高級玻璃・民國82年", 1993, 24.8001, 120.9478,
    "中埔里牛埔路239號", "路段概略", "理化醫學用玻璃儀器、安瓿管、特殊瓶", 28, "民82年名錄；代表人林孝中")

json.dump({"type": "FeatureCollection", "features": feat},
          open(os.path.join(HERE, "data", "factories.geojson"), "w", encoding="utf-8"), ensure_ascii=False)
# 內嵌版：index.html 用 <script> 載入，雙擊開檔（file://）也能用，不需要伺服器
fac_json = {"type": "FeatureCollection", "features": feat}
agg_json = json.loads(agg.to_json())
with open(os.path.join(HERE, "data", "data.js"), "w", encoding="utf-8") as fh:
    fh.write("window.STORY_DATA = " + json.dumps({"agg": agg_json, "fac": fac_json}, ensure_ascii=False) + ";" + chr(10))
print(len(agg), "groups;", [(f["properties"]["id"], f["geometry"]["coordinates"]) for f in feat])
