import os
import pandas as pd
import json

def main():
    data_dir = "data"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    csv_files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
    data_path = os.path.join(data_dir, csv_files[0])
    
    df = pd.read_csv(data_path)
    original_rows = len(df)

    duplicate_count = df.duplicated().sum()
    empty_customer_count = df["Customer ID"].isna().sum()
    invalid_quantity_count = (df["Quantity"] <= 0).sum()
    invalid_price_count = (df["Price"] <= 0).sum()

    df = df.drop_duplicates()
    df = df.dropna(subset=["Customer ID"])
    df = df[df["Quantity"] > 0]
    df = df[df["Price"] > 0]
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    cleaned_rows = len(df)

    output_file = os.path.join(output_dir, "cleaned_retail.csv")
    df.to_csv(output_file, index=False, encoding="utf-8")

    summary = {
        "原始数据总行数": int(original_rows),
        "清洗后数据总行数": int(cleaned_rows),
        "删除了多少重复数据": int(duplicate_count),
        "删除了多少空客户数据": int(empty_customer_count),
        "删除了多少无效数量或价格数据": int(invalid_quantity_count + invalid_price_count)
    }

    # 打印到终端
    for k, v in summary.items():
        print(f"{k}: {v}")

    # 写入txt文件
    txt_path = os.path.join(output_dir, "summary.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        for k, v in summary.items():
            f.write(f"{k}: {v}\n")

    # 写入json文件
    json_path = os.path.join(output_dir, "summary.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()