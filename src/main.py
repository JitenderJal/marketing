import requests
import json
import os

def makeCSV(price_list = [], persent=10, no_of_products = 5, region=1):
    if len(price_list) == 0:
        print "Enter price list"
    else:
        solr = 'http://deploy.reviews42.com:9010/solr/collection1/select?q=*:*&fq=status:0&fq=online_lowest_price:[{0} TO {1}]&fq=region:%s&'%region
        require_fields = {1:'title',2:'price',3:'product_id',4:'region'}
        others = '&sort=online_lowest_price desc&wt=json&rows='+str(no_of_products)
        script_path = os.path.abspath(__file__)  # i.e. /path/to/dir/foobar.py
        script_dir = os.path.split(script_path)[0]  # i.e. /path/to/dir/
        rel_path = "../csv/region_{}.csv".format(region)
        abs_file_path = os.path.join(script_dir, rel_path)
        outFile = open(
            abs_file_path,'w'
        )
        print 'price,' + ','.join(require_fields.values() * no_of_products)+'\n'
        outFile.write('price,' + ','.join(require_fields.values() * no_of_products)+'\n')
        count = 0
        for price in price_list:
            count += 1
            print count
            deviation = (price*persent)/100
            start, end = price-deviation, price+deviation
            solrQuery = solr.format(start, end) + "fl="+','.join(require_fields.values()) + others
            docs = json.loads(requests.get(url=solrQuery, auth = ('devops', 'devops')).text)['response']['docs']
            temp = []
            for doc in docs:
                temp.append(str(doc['title']))
                temp.append(str(doc['price']))
                temp.append(str(doc['product_id']))
                temp.append(str(doc['region']))
            print str(price)+','+','.join(temp)+'\n'
            outFile.write(str(price)+','+','.join(temp)+'\n')
            break
        outFile.close()

def AllRegion():
    solrQuery = 'http://deploy.reviews42.com:9010/solr/collection1/select?q=*:*&facet=true&facet.field=region&facet.mincount=-1&wt=json'
    regions = json.loads(requests.get(url=solrQuery, auth=('devops', 'devops')).text)['facet_counts']['facet_fields']['region'][::2]
    print regions
    return regions
if __name__ == "__main__":
    regions = AllRegion()
    for region in regions:
        price_list = [887,156,420,1255,861,809,860,961,909,1011,646,1231,1508,1379,2511,1009,3000,1329,685,3000,575,2501,1938,3000,955,3000,1359,290,1511,2744,2676,2310,560,1809,860,1809,1249,1590,1510,1009,3000,1510,230,650,985,1219,509,415,1610,340,1510,710,1809,899,709,1359,1510,810,899,571,1009,1249,3000,985,1508,1009,940,1249,1510,460,940,860,940,711,1159,1809,1510,1249,1590,1249,1155,1089,1909,1249,860,3000,570,1249,1220,134.5,1510.3,835,845,1249,3000,100,1510,160,1510,519,571,1510,1909,1508,534,809,1310.3,899.2,3000,134.5,940.4,1020.3,860.3,860.3,1560.4,1585.2,1249.4,509.4,1009.4,655.3,840.3,387.4,414.8,1249.4,1585.2,1510.3,850.3,3000,959.4,910.3,509.4,1155.2,1510.3,1410.3,1585.3,1209.4,1585.2,1889.3,550.3,900.3,1685.7,929.4,1369.4,2308.4,155.5,860.3,509.4,1249.4,1209.4,2309.4,930.3,620.3,100.4,1010.3,860,1054,655,550,1510,1155,860,860,1249,1510,854,1510,1475,954,3941,1909,3000,1510,3000,1276,1910,1510,335,576,960,760,3000,717,1537,2437,1276,645,2510,549,1510,761,860,1508,1009,1808,1808,470,1590,575,1110,2409,3000,1000,860,1309,860,809,1009,670,1406,3000,1510,1510,509,1510,860,1510,1510,1249,1249,1060,2680,2400,2409,710,1027,1510,1537,1510,3000,1110,1936,2510,1249,3000,1510,2510,710,1110,1309,1249,3000,2409,3000,1537,954,650,1989,282,855,670,600,3000,3000,646,1329,710,1089,1249,1000,510,1249,1249,1009,3000,1937,932,3000,2436,876,1510,1010,1276,3000,1276,1537,887,887,911,1526,1249,3000,2510,2809,2809,1000,650,3000,1249,2510,1510,1249,710,1276,1027,1010,991,1538,2017,2201,2511,1011,1277,810,664,651,1277,861,1009,675,1087,415,2320,1689,1909,2200,1588,887,560,560,1155,3000,1010,1310,887,1511,2409,1510,1276,650,530,711,1508,1277,1538,1537,645,440,809,1089,1009,809,2809,2309,1510,1249,3000,860,1379,1155,711,877,1110,1409,1510,1510,1640,1640,3000,2510,1327,1808,1327,735,1009,1276,1537,1510,2200,3000,1909,1989,887,3000,1617,3000,560,1510,1009,2550,2000,2540,850,2500,1500,980,1899,1290,1239,1500,1290,860,1276,230,1590,1510,1989,3000,860,860,1107,967,3000,2810,910,1009,2429,887,809,1011,1276,850,910,960,640,1249,1276,645,810,1009,2510,3000,1276,1537,887,910,2200,1110,1609,510,1089,2308,1508,855,1239,1499.9,1899,1499.9,829.9,1099.9,3000,888,1000,1300,1537,1537,1617,1936,3000,1510,1510,1537,1910,1537,1027,1537,1537,2436,860,1107,887,1537,1000,1538,887,1909,677,1027,2039,1537,1511,1261,887,1537,870,2066,1249,1249,1510,2409,1537,1276,2557,1538,1277,1537,2529,1511,860,1510,677,1250,1276,1277,810,1538,1537,1249,27,887,1537,887,887,1537,1537,1537,3000,1249,1510,1617,1276,3000,3000,887,1537,1537,860,1027,1537,677,887,1276,933,1537,1538,1537,1537,1909,1537,1537,1276,650,460,1249,3000,1430,2436,3000,1510,1027,656,1027,1356,1936,2410,1510,3000,2581,3000,499,888,837,850,887,1537,1250,860,1250,860,2410,3000,3000,887,1909,860,3000,1276,887,1510,860,1537,1249,1249,887,629,1249,3000,860,3000,1276,162,656,887,860,860,1027,1667,1537,887,702,3000,1001,27,1537,1537,1537,1537,887,1537,3000,1667,1511,1510,1277,1249,860,860,860,1249,1249,657,1249,1000,2436,1277,1538,1277,1511,1537,1537,1537,887,1537,1537,1287,2437,1537,1274,887,887,1537,860,1249,1510,1276,1510,1537,888,1027,1537,1276,1537,1537,1027,1276,1027,1510,1249,1510,3000,1249,3000,887,656,1537,1537,1537,1537,888,1538,1538,887,887,2409,861,3000,1537,1537,860,887,1537,1537,1617,1537,639,1537,1617,1936,2436,1537,860,1249,1027,1276,887,650,1510,1276,1276,860,810,860,2409,1537,1510,1276,1590,1537,1537,2436,1249,1657,1537,1510,1510,1276,1936,887,860,1276,656,1276,1537,887,887,1537,1510,887,213,809,1537,2436,1537,1276,1658,1107,1277,887,1537,677,1249,860,860,888,1510,2579,940,1652,1511,1538,1107,887,1027,932,2436,1508,809,855,710,899,1009,510,509,2501,509,3000,2501,2501,509,2200,2526,2501,2501,2501,509,960,1909,2630,1808,575,290,615,2510,1808,549,1089,1710,1508,2979,750,3000,576,509,3000,3000,550,909,1110,1909,809,470,810,205,2501,3000,1310,1010,710,509,230,2670,1609,910,960,1010,415,909,0,2308,650,470,1010,700,760,810,810,1009,1009,1309,1310,1610,834,899,899,810,810,809,600,1009,909,1009,2501,1409,440,575,2308,460,860,509,1309,1049,1310,590,2510,1360,2620,2929,809,809,955,1009,649,1888,2501,1209,1054,809,509,910,1310,230,901,1410,509,200,2309,1009,2809,859,1009,645,609,645,1089,1808,809,1009,2501,509,3000,710,1009,1009,1009,1909,3000,1009,645,1909,955,1054,3000,670,561,809,3000,1009,956,2819,230,440,1110,910,809,535,2039,2501,130,944,2501,809,1309,710,50,3000,575,645,645,1009,1110,645,509,1009,930,909,3000,1508,910,1110,899,1508,855,809,416,1009,1010,1010,1508,760,900,854,510,645,1510,415,645,1508,900,1009,470,1808,575,509,550,1310,910,2809,415,900,760,2200,2501,2809,2809,470,810,1508,1009,1010,1609,509,160,809,2501,510,1808,760,1009,340,710,900,510,710,3000,470,809,440,1110,710,905,809,855,2200,1989,1508,890,3000,1111,910,1110,860,809,899,1009,809,710,809,1508,1588,415,1808,1256,855,1009,2501,2501,1690,2810,645,955,710,1808,1510,911,809,961,710,2501,535,509,509,470,710,910,1009,509,730,1909,960,534,899,854,809,575,854,945,1909,1094,909,854,854,2428,585,1009,509,2308,1005,2501,2501,860,909,3000,420,1049,2810,909,3000,100,729,1909,1009,540,1588,509,1009,1009,510,809,600,1510,2501,3000,470,810,710,2501,760,509,809,1009,710,510,509,575,509,1009,909,909,440,575,910,1808,645,645,645,1310,560,560,761,575,1210,1089,909,2400,2400,550,2501,2501,930,1010,835,1610,2309,645,909,2501,710,910,750,2670,2310,534,750,496,534,1054,1510,560,2510,910,1276,1590,1210,850,1537,1640,909,575,1010,887,1537,1508,2200,1054,980,1327,1250,887,2556,1717,640,1537,2436,860,1537,1508,900,760,1310,960,2308,310,645,3000,3000,2501,2501,650,1899,900,2260,1239,1499.9,1499.9,1499.9,885.7,749.9,1899,887,3000,509,2308,1249,2400,2510,2510,150,900,1510,1210,1009,509,1276,1989,887,860,2510,1027,861,1610,509,1936,1510,1276,1537,1510,629,1609,509,2501,710,809,980,1489,1009,1009,1265,1390.7,910.3,1110.3,176.4,1510.8,860.3,810.3,860.3,899.2,1009.4,650.4,809.4,2309.4,509.4,509.9,1510.3,1249.4,509.4,860.3,899.2,860.3,3000,1310.3,1510.3,760.3,860.3,1000.4,1000.4,1009.4,509.4,1310.3,1510.3,860.3,1809.4,1508.4,899.2,1009.4,1089.3,1508.9,470.3,899.2,860.3,1249.4,1508.9,629.4,2200.4,1740.2,1508.4,809.4,659.4,3000,860.3,1809.4,3000,1590.2,1989.3,809.4,1249.4,1510.3,2309.4,860.3,495.2,809.4,1249.4,879.9,710.3,1510.3,860.3,2309.5,645.4,1510.3,1190.2,2309.4,709.4,509.9,1249.4,3000,810.4,809.9,1019.3,854.3,1510.3,860.3,710.3,809.4,1510.8,1938.3,909.4,860.3,1009.4,1009.4,2400.4,1510.3,1510.3,860.3,1909.4,860.3,809.4,809.4,860.3,909.4,1249.4,1510.3,809.4,909.9,1249.4,1510.3,809.4,809.9,1210.3,1009.4,1508.9,860.3,809.9,470.3,2525.5,1510.3,645.4,835.8,1249.4,1510.3,575.3,550.3,509.4,415.3,860.3,809.9,415.3,615.2,3000,3000,1000.4,835.3,1508.9,509.9,1009.4,1610.3,909.9,509.4,1510.8,954.8,614.4,910.3,509.4,1510.3,1909.4,1249.4,909.9,1560.3,1888.3,645.4,1509.9,1110.8,1009.4,650.3,2308.4,860.3,1300.4,1009.4,1009.4,1510.3,509.4,809.4,509.9,809.4,1510.3,1809.4,599.3,675.9,1310.3,1000.4,1310.8,1808.4,670.3,470.8,944.1,710.3,605.8,1510.3,470.3,3000,2309.5,2428.8,2500.5,575.2,3000,415.3,1510.3,1510.3,2344.1,155.5,510,2630,1000,2400,650,1009,645,509,1666,183,677,2510,1110,415.3,1061,809,1510,475,1249,509,1276,1276,509,1027,1276,888,509,1027,1537,860,1249,1640,470,2501,735,835,760,1111,677,710,1600,1500,1510.3,860.3,650.4,809.4,509.4,711,650.4,3000,1510.3,1510.3,910.3,3000,1510.3,95.4,860.3,809.4,440.3,860.3,470.3,1500,1359.4,940.2,860.3,509.4,1300.4,1508.4,1010.3,860.3,105.4,1510.8,1909.4,1159.4,860.3,534.3,510.3,575.3,335.3,1510.3,1510.3,1000.4,1009.4,560.3,1510.3,534.3,1510.8,1510.3,459.4,1010.3,2310,1420.9,2309.4,1009.4,1249.4,710.3,905.2,2479.3,415.3,1009.4,1249.4,1249.4,1808.4,1249.4,1249.4,510,909.4,2309.5,1000.4,1510.3,1510.3,2309.5,809.4,509.4,879.4,860.3,710.3,1110.3,860.3,509.4,1510.3,1249.4,809.4,3000,2308.4,2309.5,3000,860.8,3000,1489.3,1638.3,415.3,2870.4,1009.4,602.8,1510.3,909.4,3000,809.4,1689.3,629.4,3000,1510.3,1510.3,1909.4,2309.4,960.3,1909.4,905.2,534.3,1159.4,1249.4,1588.3,860.3,290.4,1590.2,1508.4,1510.3,860.3,575.2,2500.5,809.4,709.4,1249.4,860.3,1508.4,160.4,954.8,899.2,1009.4,710.3,860.3,1508.4,1508.9,710.3,809.4,2500.5,509.4,899.2,710.3,629.4,940.2,575.3,415.3,1510.3,1609.4,700.8,1210.3,809.4,860.3,1134.9,860.3,1510.3,860.3,930.3,3000,809.4,1510.3,509.4,1809.4,899.7,1249.4,1249.4,1210.3,1615.2,3000,1000.4,1390.2,1510.3,1000.4,1510.3,910.3,1310.3,809.4,860.3,1040.2,1379.3,1510.3,550.3,1009.4,1329.8,560.3,1510.3,155.5,1110.3,415.3,809.9,899.2,1310.3,1210.3,954.8,360.4,809.4,710.3,1510.3,899.2,1009.4,1250.4,1409.4,1010.3,1809.4,860.3,340.4,3000,1249.4,2309.9,1009.4,1249.4,2310,889.3,600.2,710.3,3000,860.3,809.4,909.4,1585.2,809.4,1249.4,1510.3,809.4,685.3,909,509.4,1359.4,1585.7,509.4,549.3,910,710.8,1110.3,550.3,830.8,860.3,1510.3,860.8,585.2,900.3,1590.2,1585.2,860.3,650.3,3000,860.3,650.4,2500.5,155.5,1510.3,1720.6,1110.8,1009.9,1508.9,1510,710,1460,475,1690,899,1010,1055,760,1249,3000,2370,860,1000,2501,810,710,3000,575,899,1540,560,710,2809,509,415,1010,1009,2501,470,540,809,509,575,509,930,415,2510,809,899,2579,1510,3000,810,1210,2310,3000,1009,809,3000,809,899,810,1010,3000,645,810,3000,3000,1588,2501,1910,1009,809,810,1330,899,1210,1089,2308,1009.4,1010,810,1508,645,1009,410,899,650,581,1511,2409,1510,2309,1508,509,3000,2510,645,1009,1310,710,645,809,510,835,1009,1909,809,760,1250,1508,910,860,645,1310,1080,1000,1000,1009,710,470,1249,3000,710,809,509,1010,909,1510,1640,1009,1510,560,1508,2511,1009,1110,1249,1110,1204.3,809,645,860,860,1510,575,650,340,1010,2529,1508,809,3000,1310,550,760,645,1508,955,809,1205,860,3000,1509,1000,1510,835,1054,2400,860,1250,1609,809,889,670,1249,1510,3000,1809,3000,3000,2520,900,1010,1160,1510,1510,809,1249,1034,1110,1001,2409,860,3000,560,1300,510,899,471,1010,509,615,575,1909,534,1009,1249,961,1510,810,3000,600,470,3000,910,2409,3000,1080,1310,860,1510,1]
        makeCSV(price_list=price_list, region=region)