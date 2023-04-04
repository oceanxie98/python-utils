import json

def loadJson(_area):
    filename =_area+".json"
    # print(filename)
    #设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
    with open(filename, 'r', encoding='utf-8') as jr:
        res_json=json.load(jr)
        return res_json
        # print(items)

def deal_with_data(items,area):
    sum=0
    for item in items:
        temp=item.get('unit')
        # print(temp.split('元/㎡/天')[0])
        result=float(temp.split('元/㎡/天')[0])
        sum+=result
        data = {
              "地区": area,
              "单价": str(sum/len(items)*30)+"元/㎡/月",
              "数量": len(items)
        }
    print(data)
    write_to_file(area,data)

def write_to_file(filename, item):
    with open('total.json', 'a', encoding='utf-8') as fp:
        fp.write(json.dumps(item, indent=2, ensure_ascii=False) + ",")

filename_s=['jintang','cdtfxq','wuhou','jinjiang','chenghua','jinniu','qingyangqu','dujiangyanshi','xindu','qingbaijiang','pixian','wenjiang','longquanyi','shuangliu','cdgaoxin','gaoxinxiqu','xinjin','cdqls','chengdu','cdchongzhou','cddayi','cdpujiang']
for filenema1 in filename_s:
    temp1=loadJson(filenema1)
    deal_with_data(temp1,filenema1)