def is_position_safe(pos, obstacles):
    """
    检查给定位置是否与障碍物列表中的任何障碍物重叠。

    :param pos: 要检查的位置，格式为 (x, y)。
    :param obstacles: 障碍物列表，每个障碍物都是一个 pygame.Rect 对象。
    :return: 如果位置安全（不与障碍物重叠），则返回 True；否则返回 False。
    """
    player_rect = pygame.Rect(pos[0], pos[1], player_width, player_height)  # 假设 player_width 和 player_height 已定义
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            return False
    return True


def find_safe_position(obstacles, map_size):
    """
    在地图上找到一个安全的生成位置。

    :param obstacles: 障碍物列表。
    :param map_size: 地图大小，格式为 (width, height)。
    :return: 安全的位置坐标，格式为 (x, y)。
    """
    while True:
        # 随机生成一个位置
        x = random.randint(0, map_size[0] - player_width)
        y = random.randint(0, map_size[1] - player_height)
        if is_position_safe((x, y), obstacles):
            return x, y  # 找到安全位置，返回坐标

# 假设 map_size 是地图的宽度和高度
# 在玩家接入服务器时调用这个函数来生成玩家
safe_position = find_safe_position(self.obstacles, map_size)
player = Player(safe_position[0], safe_position[1])
