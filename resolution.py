def is_variable(x):
    """判断是否为变量（以小写字母开头）"""
    return isinstance(x, str) and x.islower()

def is_function(x):
    """判断是否为 Skolem 函数（以小写字母开头的元组），与谓词进行区分"""
    return isinstance(x, tuple) and len(x) > 0 and isinstance(x[0], str) and x[0].islower()

def unify(p1, p2, subst=None):
    """合一算法：寻找使 p1 和 p2 相同的最一般置换"""
    if subst is None:
        subst = {}
    
    # 情况 1：两个项已经完全相同，直接返回当前置换
    if p1 == p2:
        return subst
    
    # 情况 2：p1 是变量，调用变量合一函数
    if is_variable(p1):
        return unify_var(p1, p2, subst)
    
    # 情况 3：p2 是变量，调用变量合一函数
    if is_variable(p2):
        return unify_var(p2, p1, subst)
    
    # 情况 4：两个都是 Skolem 函数，递归合一每个参数
    if is_function(p1) and is_function(p2):
        if len(p1) != len(p2) or p1[0] != p2[0]:
            return None
        for a, b in zip(p1[1:], p2[1:]):
            subst = unify(a, b, subst)
            if subst is None:
                return None
        return subst
    
    # 情况 5：两个都是谓词，递归合一每个参数
    if isinstance(p1, tuple) and isinstance(p2, tuple):
        if len(p1) != len(p2) or p1[0] != p2[0]:
            return None
        # 遍历两个谓词的所有参数，递归合一每一对参数
        # 若任意一对参数合一失败，返回 None
        # 所有参数合一成功后，返回最终的 subst
        for a, b in zip(p1[1:], p2[1:]):
            subst = unify(a, b, subst)
            if subst is None:
                return None
        return subst
    
    # 其他情况（如不同常量），不可合一
    return None

def unify_var(var, x, subst):
    """处理变量的合一"""
    # 情况 1：变量 var 已经有置换，用置换后的项继续合一
    if var in subst:
        return unify(subst[var], x, subst)
    
    # 情况 2：x 是变量且已经有置换，用置换后的项继续合一
    if x in subst:
        return unify(var, subst[x], subst)
    
    # 发生检查：避免变量出现在替换项中
    if occurs_check(var, x, subst):
        return None
    subst[var] = x
    return subst

def occurs_check(var, x, subst):
    """发生检查：防止循环置换"""
    if var == x:
        return True
    if is_variable(x) and x in subst:
        return occurs_check(var, subst[x], subst)
    if is_function(x) or isinstance(x, tuple):
        return any(occurs_check(var, arg, subst) for arg in x[1:])
    return False

def apply_subst(lit, subst):
    """对子句中的文字应用置换"""
    if is_variable(lit):
        return subst.get(lit, lit)
    if is_function(lit) or isinstance(lit, tuple):
        return tuple(apply_subst(arg, subst) for arg in lit)
    return lit

def resolve(c1, c2):
    """两个子句的归结操作"""
    for i, lit1 in enumerate(c1):
        for j, lit2 in enumerate(c2):
            # 检查是否为互补文字
            # 步骤 1：检查两个文字是否为互补对（一个有'¬'，一个没有）
            # 步骤 2：提取两个文字的谓词部分（去掉'¬'符号）
            # 步骤 3：尝试合一两个谓词部分
            # 步骤 4：若合一成功，对两个子句中除互补文字外的所有文字应用置换
            # 步骤 5：合并剩余文字，去重后返回新子句
            
            # 检查 lit1 是否有否定符号
            lit1_neg = lit1[0] == '¬' if isinstance(lit1, tuple) and len(lit1) > 0 and lit1[0] == '¬' else False
            lit2_neg = lit2[0] == '¬' if isinstance(lit2, tuple) and len(lit2) > 0 and lit2[0] == '¬' else False
            
            # 步骤 1：检查是否为互补对（一个有¬，一个没有）
            if lit1_neg != lit2_neg:
                # 步骤 2：提取谓词部分（去掉¬符号）
                if lit1_neg:
                    pred1 = lit1[1:]
                    pred2 = lit2
                else:
                    pred1 = lit1
                    pred2 = lit2[1:]
                
                # 步骤 3：尝试合一两个谓词
                subst = unify(pred1, pred2, {})
                
                # 步骤 4：若合一成功，对剩余文字应用置换
                if subst is not None:
                    # 获取 c1 中除了 lit1 之外的所有文字
                    remaining_c1 = [apply_subst(lit, subst) for k, lit in enumerate(c1) if k != i]
                    # 获取 c2 中除了 lit2 之外的所有文字
                    remaining_c2 = [apply_subst(lit, subst) for k, lit in enumerate(c2) if k != j]
                    
                    # 步骤 5：合并剩余文字，去重
                    resolvent = []
                    seen = set()
                    for lit in remaining_c1 + remaining_c2:
                        # 将文字转换为可哈希的形式
                        lit_key = str(lit)
                        if lit_key not in seen:
                            seen.add(lit_key)
                            resolvent.append(lit)
                    
                    return resolvent
    
    return None

def resolution(clauses, verbose=True):
    """完整的归结推理过程，verbose=True 时输出详细步骤"""
    if verbose:
        print("初始子句集：")
        for i, clause in enumerate(clauses):
            print(f"  {i+1}. {clause}")
        print("\n开始归结：")
    
    step = 1
    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j], i, j) for i in range(n) for j in range(i+1, n)]
        
        for (c1, c2, idx1, idx2) in pairs:
            resolvent = resolve(c1, c2)
            if resolvent == []:
                if verbose:
                    print(f"步骤{step}: 子句{idx1+1}与子句{idx2+1}归结，得到空子句□")
                    print("\n推理成功：结论成立")
                return True
            if resolvent is not None and resolvent not in clauses:
                if verbose:
                    print(f"步骤{step}: 子句{idx1+1}与子句{idx2+1}归结，得到新子句：{resolvent}")
                clauses.append(resolvent)
                step += 1
                break
        else:
            if verbose:
                print("\n推理失败：无法推出空子句，结论不成立")
            return False

# 测试案例
if __name__ == "__main__":
    print("=== 基础案例 1：计算机专业学生学 C 语言 ===")
    clauses1 = [
        [('¬', 'ComputerMajor', 'x'), ('LearnC', 'x')],
        [('ComputerMajor', 'Xiaoming')],
        [('¬', 'LearnC', 'Xiaoming')]
    ]
    resolution(clauses1)
    
    print("\n=== 自然语言 a:所有的猫都是动物，所有的动物都需要呼吸，因此所有的猫都需要呼吸 ===")
    clauses2 = [
        [('¬', 'Cat', 'x'), ('Animal', 'x')],
        [('¬', 'Animal', 'y'), ('Breathe', 'y')],
        [('Cat', 'a')],
        [('¬', 'Breathe', 'a')]
    ]
    resolution(clauses2)
    
    print("\n=== 自然语言 b:有些学生喜欢数学，所有喜欢数学的学生都喜欢逻辑，因此有些学生喜欢逻辑 ===")
    clauses3 = [
        [('Student', 'a')],
        [('LikeMath', 'a')],
        [('¬', 'Student', 'x'), ('¬', 'LikeMath', 'x'), ('LikeLogic', 'x')],
        [('¬', 'Student', 'y'), ('¬', 'LikeLogic', 'y')]
    ]
    resolution(clauses3)
