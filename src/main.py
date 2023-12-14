import pygame
import pygame_gui
from .ui import manager, ui_elements
from .drawing import draw_ground, draw_agents
from .wolf_simulation import Simulation
from .params import WINDOW_SIZE, Params

window = pygame.display.set_mode(WINDOW_SIZE)

# Grid and camera settings
camera_x, camera_y = 0, 0
zoom_level = 1
running = True

simulation = Simulation(Params.grid_size)

def move_camera():
    global camera_x, camera_y, zoom_level
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        camera_x = max(camera_x - 10, 0)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        camera_x += 10
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        camera_y = max(camera_y - 10, 0)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        camera_y += 10
    if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
        zoom_level = min(2, zoom_level + 0.1)
    if keys[pygame.K_MINUS]:
        zoom_level = max(0.5, zoom_level - 0.1)

def process_events():
    global running

    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False
            case pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("run/pause")
                if event.key == pygame.K_TAB:
                    simulation.step()
            case pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == ui_elements["next_step_btn"]:
                    simulation.step()
                elif event.ui_element == ui_elements["run_sim_btn"]:
                    print('run sim button pressed!')
                elif event.ui_element == ui_elements["reset_sim_btn"]:
                    print('reset sim button pressed!')
            case pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == ui_elements["steps_ps_slider"]:
                    print(event.value)
        manager.process_events(event)

def main():
    clock = pygame.time.Clock()
    def scaling_factor(zoom_level) -> tuple[float, float]:
        return((WINDOW_SIZE[0] * zoom_level, WINDOW_SIZE[1] * zoom_level))

    while running:
        process_events()
        move_camera()

        time_delta = clock.tick(60)/1000.0
        manager.update(time_delta)

        # if should perform step then update the simulation

        window.fill((255, 255, 255))
        for surface in (
            draw_ground(simulation, (camera_x, camera_y)),
            # draw_agents(simulation, (camera_x, camera_y)),
            ):
            scaled_surface = pygame.transform.scale(surface, scaling_factor(zoom_level))
            window.blit(scaled_surface, (0, 0)) # Draw surface while applying camera translation
        manager.draw_ui(window)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()