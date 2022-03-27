## 檔案說明

course.csv 為課程資訊列表

> 欄位
>> _id : 課程編號
>> title : 課程名稱
>> numRating : 評價數量
>> averageRating : 平均評價分數
>> totalVideoLengthInSeconds : 課程長度
>> createdAt : 課程建立時間
>> numSoldTickets : 參與學生數量
>> price : 優惠價
>> preOrderedPrice : 原價
>> publishTime : 課程開放時間
>> groupId : 課程主類別
>> groupTitle : 課程主類別中文名稱
>> groupName : 課程主類別英文文名稱
>> subGroupId : 課程子類別
>> subGroupTitle : 課程子類別中文名稱
>> subGroupName : 課程子類別英文文名稱


student.csv 為學生資訊列表

> 欄位
>> _id : 學生編號
>> name : 學生姓名
>> numBookmarkedCourse : 感興趣的課程數目
>> numBookmarkedIdea : 感興趣的文章數目
>> numBoughtCourse : 參與的課程數目
>> numCreation
>> numIdea : 新增文章數目
>> numTaughtCourse : 開課的數目


Link.csv 為學生與課程的關聯列表

> 欄位
>> student : 學生編號
>> course : 課程編號
>> type : 關聯的屬性，例如：學生有報名，學生有興趣，學生是這堂課的老師


## 執行方式

### 爬取參與人數最多的課程，並抓取該課程的問題討論區裡的發問學生帳號存到資料庫，因為只有參與學生可以發問。

```
python3 main.py -s top --db <db_connection_link>
```

### 根據資料庫裡學生編號，抓取網頁上學生資訊與其參與過或是感興趣的課程。

```
python3 main.py -s student --db <db_connection_link>
```

### 根據資料庫裡的課程編號，抓取網頁上的課程詳細資訊。

```
python3 main.py -s course --db <db_connection_link>
```

### 轉換課程資訊到 ＣＳＶ 檔案。

```
python3 main.py -t course --db <db_connection_link>
```

### 轉換學生資訊到 ＣＳＶ 檔案。

```
python3 main.py -t student --db <db_connection_link>
```

### 轉換學生與課程的關聯到 ＣＳＶ 檔案。

```
python3 main.py -t link --db <db_connection_link>
```