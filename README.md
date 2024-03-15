
def detect_collision(player_rect, panneau_rects):
    """
    检测玩家与告示牌之间的碰撞。

    :param player_rect: 玩家的矩形对象。
    :param panneau_rects: 包含所有告示牌矩形对象的列表。
    :return: 发生碰撞的告示牌索引，如果没有发生碰撞则返回 None。
    """
    for index, panneau_rect in enumerate(panneau_rects):
        if panneau_rect.colliderect(player_rect):
            return index  # 返回发生碰撞的告示牌的索引
    return None  # 如果没有发生碰撞，返回 None

# 在 main.py 的某个合适的位置调用这个函数
# 假设 player.rect 是玩家的矩形对象
collided_index = detect_collision(player.rect, panneau_rects)
if collided_index is not None:
    # 发生了碰撞，现在可以获取和显示消息了
    message_to_display = panneau[collided_index]["message"]
    self.display_sign_message(message_to_display)
