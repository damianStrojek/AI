import pygame
from time import sleep
from maze import Maze, NodeType


DELAY = 0.05  # in sec
FIELD_SIZE_X = 50
FIELD_SIZE_Y = 50

# colors
WHITE = (255, 255, 255); GRAY = (192, 192, 192); DARK_GRAY = (64, 64, 64); BLACK = (0, 0, 0)
RED = (153, 0, 0); LIGHT_RED = (192, 0, 0); BLUE = (0, 128, 255); GREEN = (0, 153, 0); BROWN = (102, 51, 0)
GOLD = (246, 187, 0)


class PyGameMaze(Maze):
    def __init__(self, maze):
        super().__init__(maze)
        # self.maze = self.maze.maze     # Quick workaround
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((len(maze[0]) * FIELD_SIZE_X, len(maze) * FIELD_SIZE_Y))
        self.assets = self.load_assets()

    @staticmethod
    def load_assets():
        assets = {}
        pit_img = pygame.image.load("assets/bricks.png").convert()
        pit_img = pygame.transform.scale(pit_img, (FIELD_SIZE_X, FIELD_SIZE_Y))
        assets['bricks'] = pit_img
        pit_img = pygame.image.load("assets/swamp.png").convert()
        pit_img = pygame.transform.scale(pit_img, (FIELD_SIZE_X, FIELD_SIZE_Y))
        assets['swamp'] = pit_img
        return assets

    def reset_env(self):
        for row_nodes in self.maze:
            for node in row_nodes:
                node.reset()

    def render(self, *args):
        self.screen.fill(WHITE)
        for row_nodes in self.maze:
            for node in row_nodes:
                self.render_node(node)
        if self.path:
            for node in self.path[1:-1]:
                self.render_node(node, on_path=True)
        pygame.display.flip()

    def render_node(self, node, on_path=False):
        def get_rect():
            return pygame.Rect(node.x * FIELD_SIZE_X, node.y * FIELD_SIZE_Y, FIELD_SIZE_X, FIELD_SIZE_Y)

        def draw_rect_alpha(surface, color):
            shape_surf = pygame.Surface(pygame.Rect(get_rect()).size, pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
            surface.blit(shape_surf, get_rect())

        if node.type == NodeType.WALL:
            self.screen.blit(self.assets['bricks'], (node.x * FIELD_SIZE_X, node.y * FIELD_SIZE_Y,
                                                     FIELD_SIZE_X, FIELD_SIZE_Y))
        else:
            if node.type == NodeType.START:
                pygame.draw.rect(self.screen, GREEN, get_rect())
            elif node.type == NodeType.GOAL:
                pygame.draw.rect(self.screen, RED, get_rect())
            elif node.type == NodeType.NORMAL:
                pygame.draw.rect(self.screen, BLACK, get_rect())
            elif node.type == NodeType.SWAMP:
                self.screen.blit(self.assets['swamp'], (node.x * FIELD_SIZE_X, node.y * FIELD_SIZE_Y,
                                                        FIELD_SIZE_X, FIELD_SIZE_Y))
            if node.parent:
                alpha = 170 if node.visited else 40
                color = (255, 255, 255, alpha) if not on_path else (GOLD[0], GOLD[1], GOLD[2], 200)
                draw_rect_alpha(self.screen, color)
        # pygame.draw.rect(self.screen, BLUE, get_rect(), 1)

    def draw(self):
        self.render()
        sleep(DELAY)


# prevent from closing immediately
def wait_for_quit():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not running:
                pygame.quit()
        sleep(0.4)
