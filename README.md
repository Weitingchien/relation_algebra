# 資料庫系統 HW #1

1. 首先執行 main.py
2. 執行後會在 D 槽建立一個 ra_cli 的資料夾，裡面有一個 ra 資料夾
3. 把 sample 資料夾裡面的.csv 檔案都放進 ra 資料夾裡
4. 開始用 SQL 語法

## Bug 待處理

1. 開頭的指令必須全部小寫，像是 select \* from classroom 的 select 必須全部小寫

## select

select \* from classroom

## project

正在新增

## rename

修改 column 名稱: alter table classroom rename column building to building_a
修改 table 名稱: alter table classroom rename to classroom_a

## set_difference

select P_Name from products_taiwan except select P_Name from products_china

## set intersection

找在台灣地區和中國大陸地區都有的商品:select P_Name from products_taiwan union select P_Name from products_china

## set_union

找台灣地區和中國大陸地區所有產品: select P_Name from products_taiwan union select P_Name from products_china

## cartesian_product

正在新增
