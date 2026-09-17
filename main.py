import pygame
import bird, pipe

pygame.init()


def start(max_fps: int = 120):
    """Run a complete Flappy Bird game."""
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    def reset_game():
        return {
            "player": bird.bird(starting_point=pygame.Vector2(110, SCREEN_HEIGHT // 2)),
            "pipes": [],
            "pipe_spawn_timer": 0.0,
            "score": 0,
            "best_score": 0,
            "started": False,
            "game_over": False,
        }

    state = reset_game()

    clouds = [
        {"x": 100 + index * 220, "y": 80 + (index % 3) * 35, "speed": 20 + index * 4}
        for index in range(5)
    ]

    font = pygame.font.SysFont("arial", 32, bold=True)
    big_font = pygame.font.SysFont("arial", 50, bold=True)

    while True:
        dt = clock.tick(max_fps) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if state["game_over"]:
                        state = reset_game()
                        continue

                    if not state["started"]:
                        state["started"] = True

                    state["player"].update(dt, jump=True)

        screen.fill((135, 206, 235))

        for cloud in clouds:
            cloud["x"] -= cloud["speed"] * dt
            if cloud["x"] < -80:
                cloud["x"] = SCREEN_WIDTH + 80
            pygame.draw.circle(screen, (255, 255, 255), (int(cloud["x"]), int(cloud["y"])), 22)
            pygame.draw.circle(screen, (255, 255, 255), (int(cloud["x"] + 30), int(cloud["y"] + 8)), 18)
            pygame.draw.circle(screen, (255, 255, 255), (int(cloud["x"] - 25), int(cloud["y"] + 8)), 18)

        ground_y = SCREEN_HEIGHT - 60
        pygame.draw.rect(screen, (119, 221, 119), (0, ground_y, SCREEN_WIDTH, 60))
        pygame.draw.rect(screen, (160, 110, 60), (0, ground_y, SCREEN_WIDTH, 5))

        if not state["game_over"] and state["started"]:
            state["player"].update(dt)
            state["pipe_spawn_timer"] += dt

            if state["pipe_spawn_timer"] >= 1.5:
                state["pipes"].append(pipe.pipe(SCREEN_WIDTH, SCREEN_HEIGHT))
                state["pipe_spawn_timer"] = 0.0

            for current_pipe in state["pipes"]:
                current_pipe.update(dt)
                if not current_pipe.scored and current_pipe.x + current_pipe.width < state["player"].pos.x:
                    current_pipe.scored = True
                    state["score"] += 1
                    state["best_score"] = max(state["best_score"], state["score"])

                if current_pipe.collides_with(state["player"]):
                    state["game_over"] = True

            state["pipes"] = [current_pipe for current_pipe in state["pipes"] if current_pipe.x + current_pipe.width > -10]

            if state["player"].pos.y + state["player"].radius >= ground_y:
                state["game_over"] = True

            if state["player"].pos.y - state["player"].radius <= 0:
                state["player"].pos.y = state["player"].radius
                state["game_over"] = True

        for current_pipe in state["pipes"]:
            current_pipe.draw()

        state["player"].draw()

        score_text = font.render(f"Score: {state['score']}", True, (255, 255, 255))
        best_text = font.render(f"Best: {state['best_score']}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))
        screen.blit(best_text, (SCREEN_WIDTH - best_text.get_width() - 20, 20))

        if not state["started"]:
            prompt = big_font.render("Press SPACE to Start", True, (255, 255, 255))
            screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 200))

        if state["game_over"]:
            game_over_text = big_font.render("Game Over", True, (255, 255, 255))
            restart_text = font.render("Press SPACE to Retry", True, (255, 255, 255))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 270))

        pygame.display.flip()


if __name__ == "__main__":
    start()

