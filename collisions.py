def collisions(player, dx, dy, walls):
    # --- 1. Handle X Axis Movement & Resolution ---
    for wall in walls:
        if player.rect.colliderect(wall):
            if dx > 0:  # Moving right, hit left side of wall
                player.pos.x = wall.left - 20
            if dx < 0:  # Moving left, hit right side of wall
                player.pos.x = wall.right + 4

    # --- 2. Handle Y Axis Movement & Resolution ---
    for wall in walls:
        if player.fall_check.colliderect(wall):
            if dy > 0:  # Moving down, hit top of wall
                player.rect.bottom = wall.top
                player.is_falling = False
                player.velocity.y = -1
            if dy < 0:  # Moving up, hit bottom of wall
                player.rect.top = wall.bottom
                player.is_falling = True
                player.velocity.y = 1
                