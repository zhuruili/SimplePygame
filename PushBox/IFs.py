#
# if 前方F1为通道:
#     小人进入到F1方格，F0变为通道或者为目的地


# if 前方F1为目的地:
#     F1修改为小人处于目的地状态，F0变为通道或者为目的地

# if 前方F1为箱子，F2为墙或为边界:
#     退出规则判断，矩阵不做任何改变


# if 前方F1为箱子，F2为通道:
#     先将F2修改为箱子，F1修改为通道，再将F1修改为小人，F0修改为通道

#
# if 前方F1为箱子，F2为目的地:
#     先将F2修改为箱子处于目的地，F1修改为通道，再将F1修改为小人，F0修改为通道

#
# if 前方F1为箱子处于目的地，F2为墙或为边界:
#     退出规则判断，矩阵不做任何改变

#
# if 前方F1为箱子处于目的地，F2为通道:
#     先将F2修改为箱子，F1修改为目的地，再将F1修改为小人处于目的地，F0修改为通道


# if 前方F1为箱子处于目的地，F2为目的地:
#     先将F2修改为箱子处于目的地，F1修改为目的地；再将F1修改为小人处于目的地，F0修改为通道






