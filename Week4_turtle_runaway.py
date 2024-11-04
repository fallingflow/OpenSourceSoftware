# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random
import time


# • Step #1) Add a timer
# • Step #2) Add your more intelligent turtle
# • Step #3) Add your concept of score

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50, start_time=0, score=0):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2
        self.start_time = time.time() # 시작 시간 기록
        self.score = score

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        # Instantiate an another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    # 시작 시간으로부터 경과한 시간을 00:00:00 format으로 출력
    def timer(self):
        elapsed_time = time.time() - self.start_time  # 경과 시간 계산
        hrs, rem = divmod(int(elapsed_time), 3600)
        mins, secs = divmod(rem, 60)
        stopwatch_format = f"{hrs:02}:{mins:02}:{secs:02}" # 00:00:00 format으로 출력
        return stopwatch_format

    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        # TODO) You can do something here and follows.
        # 100msec이 지날 때마다 self.step()을 실행한다.
        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    # is_Catched 가 False 에서 True로 변할 때 (잡을 때) 점수가 100점씩 추가된다.
    def update_score(self, old_status, new_status):
        if old_status == False and new_status == True:
            self.score += 100

    # step 함수에 이전에 못 잡은 상태인지 잡은 상태인지 함께 전달
    def step(self, is_catched=False):
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        # TODO) You can do something here and follows.
        is_catched_before = is_catched
        is_catched = self.is_catched()

        # update_score(): is_catched 가 False 에서 True로 변할 때 (잡을 때) 점수가 100점씩 추가된다.
        self.update_score(is_catched_before, is_catched)
        score = self.score

        # 게임 지속 시간
        timer = self.timer()

        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'Is catched? {is_catched}\n Time: {timer}\n Score: {score}')

        # Note) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step(is_catched), self.ai_timer_msec)

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=15, step_turn=15):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

# 무조건 chaser로부터 멀리 이동하는 알고리즘
class AwayMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=3, step_turn=3):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    # runner의 머리가 향하는 방향이 chaser와 동일하도록 하여 항상 도망치도록 함
    def run_ai(self, opp_pos, opp_heading):
        # +) 벽에 부딪히면 반사되는 각도로 다시 머리를 돌려서 screen 안에서만 움직이게.. 하고 싶었으나 잘 방법을 모르겠습니다
        chaser_pos = opp_pos
        runner_pos = self.position()

        angle = opp_heading
        self.forward(self.step_move)
        self.setheading(angle)

# class RandomMover(turtle.RawTurtle):
#     def __init__(self, canvas, step_move=10, step_turn=10):
#         super().__init__(canvas)
#         self.step_move = step_move
#         self.step_turn = step_turn
#
#     def run_ai(self, opp_pos, opp_heading):
#         mode = random.randint(0, 2)
#         if mode == 0:
#             self.forward(self.step_move)
#         elif mode == 1:
#             self.left(self.step_turn)
#         elif mode == 2:
#             self.right(self.step_turn)

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # TODO) Change the follows to your turtle if necessary
    chaser = ManualMover(screen)
    runner = AwayMover(screen) # runner 객체를 RandomMover에서 AwayMover 객체로 변경

    game = RunawayGame(screen, runner, chaser)
    game.start()
    screen.mainloop()
