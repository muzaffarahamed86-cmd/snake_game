import turtle
import time
import random

# --- Game Config ---
FOOD_COLORS = ["red", "blue", "yellow", "green"]
LEVEL_SPEED = {"Easy": 150, "Medium": 100, "Hard": 70}  # milliseconds
OBSTACLE_INTERVAL = 30  # seconds


class SnakeGame:
    def __init__(self):
        # Game State
        self.score = 0
        self.high_score = 0
        self.level = "Easy"
        self.delay = LEVEL_SPEED["Easy"]
        self.walls = True
        self.survival_mode = False
        self.direction = "stop"
        self.running = False
        self.obstacles = []
        self.last_obstacle_time = time.time()

        # --- Setup screen ---
        self.wn = turtle.Screen()
        self.wn.title("🐍 Snake Game v4.2 - Smooth Snake")
        self.wn.bgcolor("black")
        self.wn.setup(width=600, height=600)
        self.wn.tracer(0)

        # --- Create Game Elements ---
        self.create_snake()
        self.create_food()
        self.create_scoreboard()

        # --- Bind Keys ---
        self.bind_keys()

    # --- UI Elements ---
    def create_snake(self):
        self.snake = []
        for i in range(3):
            seg = turtle.Turtle(shape="circle")  # changed from "square" → "circle"
            seg.color("lime")
            seg.penup()
            seg.shapesize(stretch_wid=0.9, stretch_len=0.9)  # makes snake tighter & smoother
            seg.goto(-18 * i, 0)  # reduced gap between segments
            self.snake.append(seg)
        # make head distinct
        self.snake[0].color("limegreen")

    def create_food(self):
        self.food = turtle.Turtle()
        self.food.shape("circle")
        self.food.color(random.choice(FOOD_COLORS))
        self.food.penup()
        self.food.goto(0, 100)

    def create_scoreboard(self):
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0, 260)
        self.update_score()

    def update_score(self):
        self.pen.clear()
        self.pen.write(f"Score: {self.score}  High Score: {self.high_score}",
                       align="center", font=("Courier", 18, "bold"))

    # --- Key Bindings ---
    def bind_keys(self):
        self.wn.listen()
        self.wn.onkeypress(self.go_up, "Up")
        self.wn.onkeypress(self.go_down, "Down")
        self.wn.onkeypress(self.go_left, "Left")
        self.wn.onkeypress(self.go_right, "Right")

    # --- Movement ---
    def go_up(self):
        if self.direction != "down":
            self.direction = "up"
            self.running = True

    def go_down(self):
        if self.direction != "up":
            self.direction = "down"
            self.running = True

    def go_left(self):
        if self.direction != "right":
            self.direction = "left"
            self.running = True

    def go_right(self):
        if self.direction != "left":
            self.direction = "right"
            self.running = True

    def move(self):
        head = self.snake[0]
        x, y = head.xcor(), head.ycor()
        if self.direction == "up":
            head.sety(y + 20)
        elif self.direction == "down":
            head.sety(y - 20)
        elif self.direction == "left":
            head.setx(x - 20)
        elif self.direction == "right":
            head.setx(x + 20)

    # --- Collision Logic ---
    def check_food_collision(self):
        if self.snake[0].distance(self.food) < 20:
            self.food.goto(random.randint(-280, 280), random.randint(-280, 280))
            self.food.color(random.choice(FOOD_COLORS))

            new_segment = turtle.Turtle(shape="circle")  # smoother shape
            new_segment.color("lime")
            new_segment.penup()
            new_segment.shapesize(stretch_wid=0.9, stretch_len=0.9)
            self.snake.append(new_segment)

            self.score += 10
            if self.score > self.high_score:
                self.high_score = self.score
            self.update_score()

    def check_wall_collision(self):
        head = self.snake[0]
        if self.walls:
            if abs(head.xcor()) > 290 or abs(head.ycor()) > 290:
                return True
        else:
            # Wrap around (infinity mode)
            if head.xcor() > 290:
                head.setx(-290)
            elif head.xcor() < -290:
                head.setx(290)
            elif head.ycor() > 290:
                head.sety(-290)
            elif head.ycor() < -290:
                head.sety(290)
        return False

    def check_self_collision(self):
        head = self.snake[0]
        for segment in self.snake[1:]:
            if head.distance(segment) < 18:  # adjusted for circle size
                return True
        return False

    def check_obstacle_collision(self):
        head = self.snake[0]
        for obs in self.obstacles:
            if head.distance(obs) < 20:
                return True
        return False

    # --- Obstacle Creation ---
    def add_obstacle(self):
        obstacle = turtle.Turtle()
        obstacle.shape("square")
        obstacle.color("gray")
        obstacle.shapesize(stretch_wid=1, stretch_len=2)
        obstacle.penup()
        obstacle.goto(random.randint(-260, 260), random.randint(-260, 260))
        self.obstacles.append(obstacle)

    # --- Game Over & Restart ---
    def game_over(self):
        self.pen.goto(0, 0)
        self.pen.write(f"Game Over!\nFinal Score: {self.score}",
                       align="center", font=("Courier", 24, "bold"))
        self.wn.update()
        time.sleep(1.5)
        choice = self.wn.textinput("Game Over", "Play again? (y/n): ")
        if choice and choice.lower().startswith("y"):
            self.reset_game()
        else:
            self.wn.bye()

    def reset_game(self):
        for seg in self.snake:
            seg.hideturtle()
        for obs in self.obstacles:
            obs.hideturtle()

        self.snake.clear()
        self.obstacles.clear()
        self.score = 0
        self.update_score()

        self.create_snake()
        self.food.goto(0, 100)
        self.choose_settings()  # re-prompt for settings
        self.bind_keys()        # re-bind after prompts
        self.run_game()         # restart loop

    # --- Menu ---
    def choose_settings(self):
        # Level choice
        level_choice = self.wn.textinput("Choose Level", "Enter Easy / Medium / Hard:")
        if not level_choice:
            level_choice = "easy"
        level_choice = level_choice.lower()
        if level_choice.startswith("m"):
            self.level = "Medium"
        elif level_choice.startswith("h"):
            self.level = "Hard"
        else:
            self.level = "Easy"
        self.delay = LEVEL_SPEED[self.level]

        # Mode choice
        mode_choice = self.wn.textinput("Game Mode", "Choose Mode: Classic (with walls) / Infinite (no walls):")
        if not mode_choice:
            mode_choice = "classic"
        mode_choice = mode_choice.lower()

        if mode_choice.startswith("i"):
            self.walls = False
            survival_choice = self.wn.textinput("Survival Mode", "Enable Survival Mode? (y/n): ")
            self.survival_mode = survival_choice and survival_choice.lower().startswith("y")
        else:
            self.walls = True
            self.survival_mode = False

        self.direction = "stop"
        self.running = False
        self.bind_keys()  # re-enable controls after popup closes

    # --- Game Loop ---
    def update_snake_body(self):
        for i in range(len(self.snake) - 1, 0, -1):
            x = self.snake[i - 1].xcor()
            y = self.snake[i - 1].ycor()
            self.snake[i].goto(x, y)

    def run_game(self):
        self.wn.update()

        if self.running:
            self.update_snake_body()
            self.move()

            if self.check_wall_collision() or self.check_self_collision() or self.check_obstacle_collision():
                self.game_over()
                return

            self.check_food_collision()

            # Add obstacles in survival mode
            if self.survival_mode and (time.time() - self.last_obstacle_time > OBSTACLE_INTERVAL):
                self.add_obstacle()
                self.last_obstacle_time = time.time()

        self.wn.ontimer(self.run_game, self.delay)

    # --- Start ---
    def start(self):
        self.choose_settings()
        self.bind_keys()
        self.run_game()
        self.wn.mainloop()


# --- Run Game ---
if __name__ == "__main__":
    SnakeGame().start()
