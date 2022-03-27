# 檔案說明

course.csv 為課程資訊列表

student.csv 為學生資訊列表

Link.csv 為學生與課程的關聯列表


# 執行方式

## 爬取參與人數最多的課程，並抓取該課程的問題討論區裡的發問學生帳號存到資料庫，因為只有參與學生可以發問。

```
python3 main.py -s top --db <db_connection_link>
```

## 根據資料庫裡學生編號，抓取網頁上學生資訊與其參與過或是感興趣的課程。

```
python3 main.py -s student --db <db_connection_link>
```

## 根據資料庫裡的課程編號，抓取網頁上的課程詳細資訊。

```
python3 main.py -s course --db <db_connection_link>
```

## 轉換課程資訊到 ＣＳＶ 檔案。

```
python3 main.py -t course --db <db_connection_link>
```

## 轉換學生資訊到 ＣＳＶ 檔案。

```
python3 main.py -t student --db <db_connection_link>
```

## 轉換學生與課程的關聯到 ＣＳＶ 檔案。

```
python3 main.py -t link --db <db_connection_link>
```