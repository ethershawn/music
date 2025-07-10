### 07.10.2025 Hindemith Chord Classification Tool by LI Dongwei.
### ethershawn@foxmail.com


import re
from itertools import combinations

def process_elements(elements):
    # 生成所有有序组合 (i < j)
    seen_pairs = set()  # 用于跟踪已见过的组合
    pairs = []          # 存储最终的有序组合
    
    # 遍历所有可能的索引组合 (i, j) 其中 i < j
    for i in range(len(elements)):
        for j in range(i + 1, len(elements)):
            a, b = elements[i], elements[j]
            
            # 跳过元素相同的组合
            if a == b:
                continue
            
            # 检查是否已处理过这对元素（避免重复计算）
            pair_key = (a, b)
            if pair_key in seen_pairs:
                continue
                
            seen_pairs.add(pair_key)
            pairs.append((a, b))
    
    # 计算差值并分组
    group_orders = {
        "P": (7, 5),
        "M": (4, 8),
        "N": (3, 9),
        "S": (2, 10),
        "D": (1, 11),
        "T": (6,)
    }
    group_dict = {g: [] for g in group_orders}
    
    for a, b in pairs:
        diff = (b - a) % 12
        result_str = f"<{a},{b}>= {diff}"
        for group, values in group_orders.items():
            if diff in values:
                group_dict[group].append((diff, result_str))
                break
        else:  # 默认归入P组
            group_dict["P"].append((diff, result_str))
    
    # 按组内顺序排序
    for group in group_dict:
        group_dict[group].sort(key=lambda x: group_orders[group].index(x[0]))
    
    # 构建结果集
    results = []
    r_value = None
    first_group_found = False
    
    for group in "PMNSDT":
        if not group_dict[group]: continue
        
        for idx, (diff, res_str) in enumerate(group_dict[group]):
            if not first_group_found:
                first_group_found = True
                a, b = re.match(r"<(\d+),(\d+)>=", res_str).groups()
                a, b = int(a), int(b)
                
                # 计算R值
                if group == "P":
                    r_value = a if diff == 7 else b if diff == 5 else None
                elif group == "M":
                    r_value = a if diff == 4 else b if diff == 8 else None
                elif group == "N":
                    r_value = a if diff == 3 else b if diff == 9 else None
                elif group == "S":
                    r_value = a if diff == 10 else b if diff == 2 else None
                elif group == "D":
                    r_value = a if diff == 11 else b if diff == 1 else None
                
                results.append(f"{res_str} ({group})" + (f" R = {r_value}" if r_value is not None else ""))
            else:
                results.append(f"{res_str} ({group})")
    
   
    # 分类逻辑
    all_diffs = [diff for group in group_dict.values() for diff, _ in group]
    t_count = all_diffs.count(6)
    classification = "VI"  # 先这样写吧，实际上就四个

    if 6 not in all_diffs:
        # V类判断 
        if (set(diff for diff, _ in group_dict["P"]) == {5} and
            set(diff for diff, _ in group_dict["S"]) == {10} and
            not any(group_dict[g] for g in "MNDT")):
            classification = "V"
        
        # V类判断
        elif (set(diff for diff, _ in group_dict["M"]) == {4, 8} and
              not any(group_dict[g] for g in "PNSDT")):
            classification = "V"
        
        # I类
        elif not any(d in all_diffs for d in [2,10,1,11,6]):
            classification = "I"
        
        # III类
        elif any(d in all_diffs for d in [2,10,1,11]):
            classification = "III"
    else:
        if (10 in all_diffs and not any(d in all_diffs for d in [1,11,2]) and 
            r_value == elements[0]):
            classification = "IIa"
        elif any(d in all_diffs for d in [2,10]) and not any(d in all_diffs for d in [1,11]):
            classification = "IIb"
            if t_count >= 2:
                classification += ".3"
            elif r_value == elements[0]:
                classification += ".1"
            else:
                classification += ".2"
        elif any(d in all_diffs for d in [1,11]):
            classification = "IV"
    
    # 添加子分类
    if classification in ["I", "IIb", "III", "IV"] and not classification.endswith((".1", ".2", ".3")):
        classification += ".1" if r_value == elements[0] else ".2"
    
    # V/VI类特殊处理
    if classification in ["V", "VI"] and results:
        results[0] = re.sub(r" R = \d+", " R = None", results[0])
    
    # 输出结果
    print("\n处理结果：")
    for res in results:
        print(res)
    print(f"\n分类：{classification}\n\n")

def main():
    # 显示程序标题
    print("\n07.10.2025 Hindemith Chord Classification Tool by LI Dongwei.\n")
    
    print("请输入和弦材料（数字记写，由低到高，以空格区分），输入 'exit' 退出程序：")
    while True:
        user_input = input("请输入数字： ").strip()
        if user_input.lower() == 'exit':
            print("程序已退出。")
            break
            
        # 检查输入是否为空
        if not user_input:
            print("输入不能为空，请重新输入。")
            continue
            
        try:
            elements = list(map(int, user_input.split()))
            process_elements(elements)
        except ValueError:
            print("输入无效，请输入有效的数字或 'exit'。")

if __name__ == "__main__":
    main()
