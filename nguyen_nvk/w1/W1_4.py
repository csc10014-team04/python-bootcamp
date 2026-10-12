def transpose_comprehension(matrix: list[list]) -> list[list]:
    if not matrix or not matrix[0]:
        return []
    
    rows = len(matrix)
    cols = len(matrix[0])
    
    return [[matrix[j][i] for j in range(rows)] for i in range(cols)]