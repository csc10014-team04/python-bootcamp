def rotate_matrix(matrix):
    res=[]
    for col in range(len(matrix[0])):
        row=[]
        for i in range(len(matrix)-1,-1,-1):
            row.append(matrix[i][col])
        res.append(row)
    return res