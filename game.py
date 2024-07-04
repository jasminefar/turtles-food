import turtle
import random
import time

# this game is a game where the turtle catches the food

class GameScreen:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.bgcolor("lightblue")
        self.screen.title("Turtles Food")
        self.screen.setup(width=800, height=600)
        self.screen.tracer(0)

class Player:
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.shape("turtle")
        self.turtle.color("green")
        self.turtle.penup()
        self.turtle.speed(0)
        self.turtle.goto(0, -250)
        self.turtle.direction = "stop"
        self.speed = 20
        
    def go_left(self):
        self.turtle.direction = "left"
        
    def go_right(self):
        self.turtle.direction = "right"
        
    def move(self):
        if self.turtle.direction == "left":
            x = self.turtle.xcor()
            x -= self.speed
            if x < -390:
                x = -390
            self.turtle.setx(x)
        if self.turtle.direction == "right":
            x = self.turtle.xcor()
            x += self.speed
            if x > 390:
                x = 390
            self.turtle.setx(x)
    
    def reset(self):
        self.turtle.goto(0, -250)
        self.turtle.direction = "stop"

class Food:
    def __init__(self):
        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("circle")
        self.food.color("red")
        self.food.penup()
        self.food.goto(0, 250)
        self.food.speed = random.randint(2, 5)

    def move(self):
        y = self.food.ycor()
        y -= self.food.speed
        self.food.sety(y)
        if y < -300:
            self.food.goto(random.randint(-390, 390), 250)
            self.food.speed = random.randint(2, 5)
    
    def reset(self):
        self.food.goto(random.randint(-390, 390), 250)
        self.food.speed = random.randint(2, 5)

class PowerUp:
    def __init__(self):
        self.powerup = turtle.Turtle()
        self.powerup.speed(0)
        self.powerup.shape("square")
        self.powerup.color("blue")
        self.powerup.penup()
        self.powerup.goto(0, 250)
        self.powerup.speed = random.randint(2, 5)

    def move(self):
        y = self.powerup.ycor()
        y -= self.powerup.speed
        self.powerup.sety(y)
        if y < -300:
            self.powerup.goto(random.randint(-390, 390), 250)
            self.powerup.speed = random.randint(2, 5)
    
    def reset(self):
        self.powerup.goto(random.randint(-390, 390), 250)
        self.powerup.speed = random.randint(2, 5)

class Obstacle:
    def __init__(self):
        self.obstacle = turtle.Turtle()
        self.obstacle.speed(0)
        self.obstacle.shape("square")
        self.obstacle.color("black")
        self.obstacle.shapesize(stretch_wid=1, stretch_len=2)
        self.obstacle.penup()
        self.obstacle.goto(random.randint(-390, 390), random.randint(-300, 300))
        self.obstacle.speed = random.randint(2, 5)
    
    def move(self):
        y = self.obstacle.ycor()
        y -= self.obstacle.speed
        self.obstacle.sety(y)
        if y < -300:
            self.obstacle.goto(random.randint(-390, 390), random.randint(300, 600))
            self.obstacle.speed = random.randint(2, 5)
    
    def reset(self):
        self.obstacle.goto(random.randint(-390, 390), random.randint(300, 600))
        self.obstacle.speed = random.randint(2, 5)

class Score:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.score_display = turtle.Turtle()
        self.score_display.speed(0)
        self.score_display.color("black")
        self.score_display.penup()
        self.score_display.hideturtle()
        self.score_display.goto(0, 260)
        self.update_score()

    def update_score(self):
        self.score_display.clear()
        self.score_display.write(f"Score: {self.score}  High Score: {self.high_score}  Level: {self.level}", align="center", font=("Courier", 24, "normal"))
        
    def increase_score(self):
        self.score += 10
        if self.score > self.high_score:
            self.high_score = self.score
        self.update_score()

    def reset_score(self):
        self.score = 0
        self.update_score()

    def next_level(self):
        self.level += 1
        self.update_score()

class Game:
    def __init__(self):
        self.screen = GameScreen()
        self.player = Player()
        self.foods = [Food() for _ in range(10)]
        self.powerups = [PowerUp() for _ in range(3)]
        self.obstacles = [Obstacle() for _ in range(5)]
        self.score = Score()
        self.screen.screen.listen()
        self.screen.screen.onkeypress(self.player.go_left, "Left")
        self.screen.screen.onkeypress(self.player.go_right, "Right")
        self.running = True
        self.start_time = time.time()
        self.speed_boost = False
        self.boost_time = 0
        
    def check_collision(self):
        for food in self.foods:
            if self.player.turtle.distance(food.food) < 20:
                self.score.increase_score()
                food.reset()
        
        for powerup in self.powerups:
            if self.player.turtle.distance(powerup.powerup) < 20:
                self.speed_boost = True
                self.boost_time = time.time()
                self.player.speed = 40
                powerup.reset()
        
        for obstacle in self.obstacles:
            if self.player.turtle.distance(obstacle.obstacle) < 20:
                self.game_over()

    def game_over(self):
        self.score.reset_score()
        self.player.reset()
        for food in self.foods:
            food.reset()
        for powerup in self.powerups:
            powerup.reset()
        for obstacle in self.obstacles:
            obstacle.reset()
        self.start_time = time.time()
        self.player.speed = 20
        self.speed_boost = False
        self.score.level = 1
        self.score.update_score()

    def level_up(self):
        self.score.next_level()
        for food in self.foods:
            food.food.speed += 1
        for powerup in self.powerups:
            powerup.powerup.speed += 1
        for obstacle in self.obstacles:
            obstacle.obstacle.speed += 1
        self.start_time = time.time()

    def run(self):
        while self.running:
            self.screen.screen.update()
            self.player.move()
            for food in self.foods:
                food.move()
            for powerup in self.powerups:
                powerup.move()
            for obstacle in self.obstacles:
                obstacle.move()
            self.check_collision()
            if self.speed_boost and time.time() - self.boost_time > 5:
                self.player.speed = 20
                self.speed_boost = False
            if time.time() - self.start_time > 60:
                self.level_up()
            time.sleep(0.02)

if __name__ == "__main__":
    game = Game()
    game.run()
    turtle.done()
