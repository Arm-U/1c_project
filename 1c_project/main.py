import cv2

# read image
img = cv2.imread('image.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh, img = cv2.threshold(img, 127, 1, cv2.THRESH_BINARY)

# find first point of our board, which is nearest to left-upper edge
first_x, first_y = -1, -1
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        if img[i][j] == 0:
            first_x, first_y = i, j
            break
    if (first_x, first_y) != (-1, -1):
        break

# find width of line
width = 0
for i in range(img.shape[1]):
    if img[first_x][first_y + i] == 1:
        break
    width += 1

# find len of first part of line
edge_1_1 = 0
for i in range(img.shape[0]):
    if img[first_x + i][first_y - 1] == 0:
        break
    edge_1_1 += 1

# find len of middle part of line
edge_1_2 = 0
for i in range(img.shape[0]):
    if img[first_x + width + edge_1_1 + i][first_y - 1] == 0:
        break
    edge_1_2 += 1

print(width, edge_1_1, edge_1_2)

centre_x_1_1 = first_x + (edge_1_1 // 2)
centre_y_1_1 = first_y - (edge_1_1 // 2)
step = (edge_1_1 // 2) + width + (edge_1_2 // 2)

# checks having X in i, j sector
def is_x(i, j):
    if img[centre_x_1_1 + i * step][centre_y_1_1 + j * step] == 0:
        return True
    return False

# checks having O in i, j sector
def is_o(i, j):
    centre_x = centre_x_1_1 + i * step
    centre_y = centre_y_1_1 + j * step

    len = edge_1_1 // 4
    if j == 1:
        len = edge_1_2 // 4

    centre_y += len

    for k in range(len):
        if img[centre_x][centre_y + k] == 0:
            return True

    return False

board = [[0 for x in range(3)] for y in range(3)]
for i in range(3):
    for j in range(3):
        board[i][j] = 0

        if is_o(i, j):
            board[i][j] = -1

        if is_x(i, j):
            board[i][j] = 1

def have_line(my_board):
    for i in range(3):
        sum = my_board[i][0] + my_board[i][1] + my_board[i][2]
        if sum == 3 or sum == -3:
            return (i, 0, i, 2)

    for i in range(3):
        sum = my_board[0][i] + my_board[1][i] + my_board[2][i]
        if sum == 3 or sum == -3:
            return (0, i, 2, i)

    sum = my_board[0][0] + my_board[1][1] + my_board[2][2]
    if sum == 3 or sum == -3:
        return (0, 0, 2, 2)

    sum = my_board[0][2] + my_board[1][1] + my_board[0][2]
    if sum == 3 or sum == -3:
        return (0, 2, 2, 0)

    return False


