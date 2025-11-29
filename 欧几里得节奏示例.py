def E_debug(k, n):
    """
    欧几里得节奏算法 (带调试输出)
    将k个脉冲均匀分布在n个时值中
    
    参数:
        k: 重拍数量 (脉冲数)
        n: 总时值长度
    
    返回:
        list: 由0和1组成的节奏序列
    """
    print(f"=== 欧几里得节奏算法 E({k}, {n}) ===")
    print(f"目标: 将 {k} 个重拍均匀分布在 {n} 个时值中")
    print()
    
    # 初始化：创建k个[1]和(n-k)个[0]
    s = [[1] if i < k else [0] for i in range(n)]
    print(f"步骤 0 - 初始化:")
    print(f"  序列 s = {s}")
    print(f"  可视化: {''.join(str(item[0]) for item in s)}")
    print()

    # 计算初始参数
    d = n - k  # 0的数量
    n_val = max(k, d)  # 较大的分组长度
    k_val = min(k, d)  # 较小的分组长度
    z = d  # 剩余需要处理的0的数量
    
    step = 1
    
    # 迭代处理，直到所有分组完成
    while z > 0 or k_val > 1:
        print(f"步骤 {step} - 开始迭代:")
        print(f"  当前参数: z={z}, k={k_val}, n={n_val}, d={d}")
        print(f"  当前序列: {s}")
        
        # 将后k个序列附加到前k个序列后面
        print(f"  操作: 将后 {k_val} 个序列附加到前 {k_val} 个序列后面")
        for i in range(k_val):
            print(f"    s[{i}].extend(s[{len(s) - 1 - i}])")
            s[i].extend(s[len(s) - 1 - i])
        
        # 删除已经处理过的后k个序列
        print(f"  操作: 删除后 {k_val} 个序列")
        s = s[:-k_val]
        print(f"  更新后序列: {s}")
        
        # 更新参数
        z = z - k_val      # 减少剩余0的数量
        d = n_val - k_val  # 计算新的差值
        n_val = max(k_val, d)  # 更新较大的分组长度
        k_val = min(k_val, d)  # 更新较小的分组长度
        
        print(f"  更新后参数: z={z}, k={k_val}, n={n_val}, d={d}")
        
        # 可视化当前状态
        flat_sequence = []
        for sublist in s:
            flat_sequence.extend(sublist)
        print(f"  当前节奏: {''.join(map(str, flat_sequence))}")
        print()
        
        step += 1

    print("=== 算法完成 ===")
    
    # 将嵌套列表展平为一维序列
    result = [item for sublist in s for item in sublist]
    return result


# 示例运行
if __name__ == "__main__":
    print("开始执行欧几里得节奏算法...")
    print()
    
    rhythm = E_debug(5, 13)
    rhythm_str = ''.join(map(str, rhythm))
    
    print("最终结果:")
    print(f"欧几里得节奏 E(5,13): {rhythm_str}")
    
    print("\n节奏解析:")
    print(f"总长度: {len(rhythm_str)} 个时值")
    print(f"重拍数: {sum(int(x) for x in rhythm_str)} 个脉冲")
    
    print("\n节奏模式可视化:")
    for i, beat in enumerate(rhythm_str):
        if beat == '1':
            print('X', end=' ')  # 重拍
        else:
            print('.', end=' ')  # 轻拍
    print()
    
    print("\n时间位置:")
    for i, beat in enumerate(rhythm_str):
        if beat == '1':
            print(f"位置 {i}: 重拍")
