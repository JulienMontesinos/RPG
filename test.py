def action_mouse(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        # 设置目标位置
        self.target_x, self.target_y = event.pos

def update(self):
    # 检查是否需要向目标位置移动
    if self.x < self.target_x:
        self.move_right()
        self.current_dir = "right"
        self.change_animation("right")
    elif self.x > self.target_x:
        self.move_left()
        self.current_dir = "left"
        self.change_animation("left")

    if self.y < self.target_y:
        self.move_up()
        self.current_dir = "up"
        self.change_animation("up")
    elif self.y > self.target_y:
        self.move_down()
        self.current_dir = "down"
        self.change_animation("down")

def move_right(self):
    # 移动角色并限制速度，避免一次跳到目标位置
    self.x += min(self.speed, self.target_x - self.x)

def move_left(self):
    self.x -= min(self.speed, self.x - self.target_x)

def move_up(self):
    self.y -= min(self.speed, self.y - self.target_y)

def move_down(self):
    self.y += min(self.speed, self.target_y - self.y)
